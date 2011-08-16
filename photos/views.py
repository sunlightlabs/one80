from django.shortcuts import get_object_or_404, render
from one80.committees.models import Hearing

def photo_detail(request, slug, photo_id):
    
    hearing = get_object_or_404(Hearing, slug=slug)
    photo = hearing.photos.get(pk=photo_id)
    
    photos = hearing.photos.filter(name__lt=photo.name).order_by('-name')
    previous_photo = photos[0] if len(photos) > 0 else None
    
    photos = hearing.photos.filter(name__gt=photo.name).order_by('name')
    next_photo = photos[0] if len(photos) > 0 else None
    
    context = {
        'hearing': hearing,
        'photo': photo,
        'fullsize': photo.get_size(1000),
        'previous_photo': previous_photo,
        'next_photo': next_photo,
    }
    return render(request, "photos/photo_detail.html", context)