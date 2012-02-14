from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import Count
from django.shortcuts import render
from haystack.query import SearchQuerySet

from one80.committees.models import Committee, Hearing
from one80.people.models import Person
from one80.photos.models import Photo, Annotation

def index(request):
    hearings = Hearing.objects.published().select_related()
    context = {
        'latest_hearings': hearings[:3],
        # 'latest_annotations': Annotation.objects.published().select_related()[:3],
        # 'committees': Committee.objects.all().select_related(),
        # 'featured_photo': hearings[0].photos.all()[0],
        'leaderboard': Person.objects.with_counts(min_tags=1)[:5]
    }

    return render(request, 'index.html', context)

def contact(request):
    if request.POST:
        name = request.POST.get('feedback[name]')
        email = request.POST.get('feedback[email]')
        message = request.POST.get('feedback[message]')
        if name and email and message:
            subject = "[180] Contact from %s" % email
            if send_mail(subject, message, '%s <%s>' % (name, settings.EMAIL_FROM), [admin[1] for admin in settings.ADMINS]):
                messages.success(request, 'Thanks, your message was sent.')
            else:
                messages.error(request, 'There was an error sending your message.')
        else:
            messages.error(request, 'Please fill out all fields and try again.')

    return render(request, 'contact.html', {})