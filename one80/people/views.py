import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect

from one80.people.models import Person
from one80.search_utils import search


def person_detail(request, slug):
    person = get_object_or_404(Person, slug=slug)
    event_ids = [annot.event.id for annot in person.annotations.published(request.user)]
    recent_events = search(pk__in=event_ids).order_by('-date')[:5]
    #recent_hearings = Hearing.objects.published(request.user).filter(pk__in=hearing_ids).order_by('-start_datetime')[:5]

    context = {
        'person': person,
        'recent_events': recent_events,
    }
    return render(request, 'people/person_detail.html', context)


def leaderboard(request):
    context = {
        'leaders': Person.objects.with_counts(min_tags=1).order_by('-num_tags', 'last_name')[:100],
    }
    return render(request, 'people/leaderboard.html', context)


def search_json(request):
    query = request.GET.get('search')
    results = []
    if query:
        for result in search('people', content=query + '*'):
            try:
                results.append(result.object.to_suggest())
            except:
                pass

    return HttpResponse(json.dumps(results), content_type='application/json')
