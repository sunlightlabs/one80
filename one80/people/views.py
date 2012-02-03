import json

from django.contrib import messages
from django.db.models import Count
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render, redirect
from haystack.query import SearchQuerySet

from one80.people.models import Person
from one80.committees.models import Hearing

def person_detail(request, slug):
    person = get_object_or_404(Person, slug=slug)
    hearing_ids = [annot.hearing.id for annot in person.annotations.published(request.user)]
    recent_hearings = Hearing.objects.published(request.user).filter(pk__in=hearing_ids).order_by('-start_datetime')[:5]

    context = {
        'person': person,
        'recent_hearings': recent_hearings,
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
        sqs = SearchQuerySet().filter(result_type__exact='people', content=query+'*')
        for result in sqs:
            try:
                results.append(result.object.to_suggest())
            except:
                pass

    return HttpResponse(json.dumps(results), content_type='application/json')