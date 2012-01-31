from django.shortcuts import render

from one80.committees.models import Committee, Hearing
from one80.photos.models import Photo, Annotation

def index(request):
    hearings = Hearing.objects.published().select_related()[:10]
    context = {
        'latest_hearings': hearings,
        'latest_annotations': Annotation.objects.published().select_related()[:10],
        'committees': Committee.objects.all().select_related(),
        'featured_photo': hearings[0].photos.all()[0].sizes.all()[1],
    }
    return render(request, 'index.html', context)