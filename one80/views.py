from django.db.models import Count
from django.shortcuts import render
from haystack.query import SearchQuerySet

from one80.committees.models import Committee, Hearing
from one80.people.models import Person
from one80.photos.models import Photo, Annotation

def index(request):
    hearings = Hearing.objects.published().select_related()
    context = {
        'latest_hearings': hearings[:10],
        'latest_annotations': Annotation.objects.published().select_related()[:3],
        'committees': Committee.objects.all().select_related(),
        'featured_photo': hearings[0].photos.all()[0].sizes.all()[1],
        'leaderboard': Person.objects.with_counts(min_tags=1)[:5]
    }

    return render(request, 'index.html', context)