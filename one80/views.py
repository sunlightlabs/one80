from django.shortcuts import render

from one80.committees.models import Committee, Hearing
from one80.photos.models import Photo, Annotation

def index(request):
    context = {
        'latest_hearings': Hearing.objects.published()[:10].select_related(),
        'latest_annotations': Annotation.objects.published()[:10].select_related(),
        'committees': Committee.objects.all().select_related(),
    }
    return render(request, 'index.html', context)