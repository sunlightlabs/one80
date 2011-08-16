from django.shortcuts import get_object_or_404, render
from one80.committees.models import Hearing
from one80.photos.models import Size

def hearing_detail(request, slug):
    hearing = get_object_or_404(Hearing, slug=slug)
    # photos = [p.get_size(300, 199) for p in hearing.photos.all()] # force resize
    photos = Size.objects.filter(photo__hearing=hearing, width=300, height=199).select_related()
    context = {
        'hearing': hearing,
        'photos': photos,
    }
    return render(request, "committees/hearing_detail.html", context)