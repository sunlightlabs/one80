import datetime
import logging

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError
from django.template import loader, Context
from optparse import make_option

from postmark.models import EmailMessage
from one80.photos.models import Annotation

THRESHOLD = getattr(settings, 'ANNOTATION_MAX_QUEUE_SIZE', 5)

class Command(BaseCommand):
    args = None
    option_list = BaseCommand.option_list + (
        make_option('--sender',
            dest='sender',
            default='cron',
            help='The sender of the call; could be "cron" or "hook"'),
        )
    help = '''
           Sends notifications of new annotations.
           This is run 2 ways: crontab and post-save hook.
           If called from cron, it will only email every hour at most.
           If called from a hook, it will send if n or more new annotations are queued,
           and 5 minutes have passed since the last annotation was submitted, not more than every 20 minutes.
           '''

    def handle(self, *args, **options):
        verbosity = int(options.get('verbosity', 0))
        if verbosity == 0:
            level = logging.WARNING
        elif verbosity == 1:
            level = logging.INFO
        else:
            level = logging.DEBUG

        logging.basicConfig(level=level, format="%(message)s")
        annot_qset = Annotation.objects.unpublished().order_by('-created_date')
        try:
            last_email = EmailMessage.objects.filter(subject__startswith='[180] New annotations').order_by('-created_at')[0]
        except IndexError:
            last_email = lambda: None
            last_email.created_at=datetime.datetime(1970,1,1)
        waiting = annot_qset.filter(created_date__gt=last_email.created_at)
        send_email = False
        now = datetime.datetime.now()
        if not waiting.count():
            logging.info('No annotations queued.')
            return

        if options.get('sender') == 'hook':
            if ((waiting.count() >= THRESHOLD) and
                ((now - datetime.timedelta(minutes=20) >= last_email.created_at) or
                        (now - datetime.timedelta(minutes=5) >= waiting[1].created_date))):
                send_email = True
        else:
            if (((waiting.count() >= THRESHOLD) and now - datetime.timedelta(minutes=20) >= last_email.created_at) or
               (waiting.count() and (now - datetime.timedelta(hours=1) >= last_email.created_at))):
                send_email = True

        if not send_email:
            logging.info('Found %d queued annotations, but it\'s not time to send mail yet, skipping.' % waiting.count())
        else:
            ctx = {
                'annotations': waiting,
            }
            subject = '[180] New annotations are waiting for approval'
            message = loader.get_template('emails/new_annotations.txt').render(Context(ctx))
            if send_mail(subject,
                         message,
                         '%s <%s>' % ('180-mailer', settings.EMAIL_FROM),
                         [admin[1] for admin in settings.ADMINS]):
                logging.info('Email sent.')
