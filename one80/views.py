from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from django.shortcuts import render

from one80.search_utils import search
from one80.people.models import Person


def index(request):
    if request.GET.get('page'):
        qset = search(*settings.DEFAULT_SEARCH_MODELS, is_parent=False)
        paginator = Paginator(qset, settings.PAGINATE)
        page = request.GET.get('page', 1)
        try:
            page = paginator.page(page)
            page.object_list = [res.object for res in page.object_list]
        except InvalidPage:
            raise Http404

        context = {
            'page': page
        }

        return render(request, 'combined_list.html', context)

    else:
        events = [r.object for r in search(*settings.DEFAULT_SEARCH_MODELS, is_parent=False).order_by('-date')[:3]]
        context = {
            'latest_events': events,
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
