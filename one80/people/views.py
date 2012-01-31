import json

from django.contrib import messages
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render, redirect

from one80.people.models import Person
from one80.committees.models import Hearing

def person_detail(request, slug):
    person = get_object_or_404(Person, slug=slug)
    hearing_ids = [annot.hearing.id for annot in person.annotations.all()]
    recent_hearings = Hearing.objects.filter(pk__in=hearing_ids).order_by('-start_datetime')[:5]

    context = {
        'person': person,
        'recent_hearings': recent_hearings,
    }
    return render(request, 'people/person_detail.html', context)
