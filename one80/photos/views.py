import json

from django.contrib import messages
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.safestring import mark_safe

from one80.search_utils import search, search_one_or_404
from one80.photos.models import Annotation, Photo

DNE = "Couldn't get that annotation, does it exist?"
NOT_PERMITTED = "You don't have permission to edit annotations."

FULLSIZE_WIDTH = 882


def photo_index(request):
    pass


def photo_detail(request, slug, photo_id):
    '''Gets a photo resource for permalink display'''
    # hearing = get_object_or_404(Hearing, slug=slug)
    event = search_one_or_404('hearings', 'public events', slug=slug).object
    photo = event.photos.get(pk=photo_id)

    photos = event.photos.filter(name__lt=photo.name).order_by('-name')
    previous_photo = photos[0] if len(photos) > 0 else None

    photos = event.photos.filter(name__gt=photo.name).order_by('name')
    next_photo = photos[0] if len(photos) > 0 else None

    if request.user.is_anonymous():
        messages.warning(request, mark_safe('You need to be logged in to tag photos. <a href="/login/">Login or register now &raquo;</a>'))

    context = {
        'event': event,
        'photo': photo,
        'fullsize': photo.get_size(FULLSIZE_WIDTH),
        'annotations': photo.annotations.published(request.user),
        'previous_photo': previous_photo,
        'next_photo': next_photo,
    }
    return render(request, "photos/photo_detail.html", context)


def photo_annotations(request, slug, photo_id):
    '''Handles all photo annotation CRUD operations'''
    size = int(request.GET.get('size', FULLSIZE_WIDTH))
    action = request.GET.get('action', 'get')
    event = search_one_or_404('hearings', 'public events', slug=slug).object
    try:
        photo = event.photos.get(pk=photo_id)
    except Photo.DoesNotExist:
        raise Http404

    sized_photo = photo.get_size(size)

    cannot_edit_error = HttpResponse('You cannot edit this annotation', status=400)
    field_error = HttpResponse('Please provide all required fields', status=400)

    if action == 'save':
        try:
            id = request.GET['id']
            x = int(request.GET['left'])
            y = int(request.GET['top'])
            width = int(request.GET['width'])
            height = int(request.GET['height'])
            first = request.GET['first']
            last = request.GET['last']
            organization = request.GET['org']
            title = request.GET['title']
        except KeyError:
            return field_error
        if id == 'new':
            annot = sized_photo.create_annotation(x, y, width, height, user=request.user)
        else:
            try:
                id = int(id)
                annot = photo.annotations.get(id=id)
            except Photo.DoesNotExist:
                raise Http404

        if annot.is_editable_by(request.user):
            x, y, width, height = sized_photo.size_annotation(x, y, width, height)
            annot.x_pct = x
            annot.y_pct = y
            annot.width_pct = width
            annot.height_pct = height
            annot.first_name = first
            annot.last_name = last
            annot.title = title
            annot.organization = organization
            if request.user.is_staff:
                annot.is_public = True
            annot.save()
        else:
            return cannot_edit_error

        return HttpResponse(json.dumps(annot.to_dict(sized_photo.width, sized_photo.height, request.user)),
                            mimetype='application/json')

    elif action == 'delete':
        try:
            id = int(request.GET['id'])
            annot = photo.annotations.get(id=id)
        except KeyError:
            return field_error
        except Annotation.DoesNotExist:
            raise Http404

        if annot.is_editable_by(request.user):
            annot.delete()
            return HttpResponse(json.dumps(True), mimetype='application/json')
        else:
            return cannot_edit_error

    else:
        annotations = sized_photo.annotations_as_user(request.user)

    return HttpResponse(json.dumps(annotations),  mimetype='application/json')

def approve_annotation(request, annot_id):
    prev_page = request.META.get('HTTP_REFERER')
    if request.user.is_staff:
        try:
            annot = Annotation.objects.get(pk=int(annot_id))
            annot.is_public = True
            annot.save()
            messages.success(request, 'Annotation approved.')
        except Annotation.DoesNotExist, ValueError:
            messages.error(request, DNE)

    else:
        messages.error(request, NOT_PERMITTED)

    return redirect(prev_page)

def delete_annotation(request, annot_id):
    prev_page = request.META.get('HTTP_REFERER')
    if request.user.is_staff:
        try:
            annot = Annotation.objects.get(pk=int(annot_id))
            annot.delete()
            messages.success(request,'Annotation deleted.')
        except Annotation.DoesNotExist, ValueError:
            messages.error(request, DNE)

    else:
        messages.error(request, NOT_PERMITTED)

    return redirect(prev_page)