from django.conf import settings
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from one80.events.models import PublicEvent


def public_event_list(request):
    event_list = PublicEvent.objects.published_with_children()
    paginator = Paginator(event_list, settings.PAGINATE)
    page = request.GET.get('page', 1)
    try:
        events = paginator.page(page)
    except InvalidPage:
        raise Http404

    context = {
        'page': events,
    }

    return render(request, "events/public_event_list.html", context)


def public_event_detail(request, slug):
    event = get_object_or_404(PublicEvent, slug=slug)
    context = {
        'event': event,
    }
    if event.child_events.all().count():
        return render(request, "events/parent_event_detail.html", context)
    else:
        return render(request, "events/public_event_detail.html", context)
