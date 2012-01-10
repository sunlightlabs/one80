import datetime

from dateutil import parser
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

from one80.photos.models import Annotation

class Command(BaseCommand):
    args = None
    option_list = BaseCommand.option_list + (
        make_option('--start-date',
            dest='start_date',
            default='01/01/1970',
            help='Only include annotations created since the specified date'),
        make_option('--end-date',
            dest='end_date',
            default=datetime.datetime.now().strftime('%x %T'),
            help='Only include annotations created before the specified date'),
        )
    help = '''
           Re-crops and saves thumbnails for the specified date range
           '''

    def handle(self, *args, **options):
        start = parser.parse(options['start_date'])
        end = parser.parse(options['end_date'])
        [annot.save() for annot in Annotation.objects.filter(
                created_date__gte=start,
                created_date__lte=end)]
