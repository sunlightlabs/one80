from django.conf import settings
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from one80.committees.models import Committee, Hearing
from one80.photos.models import Size

def committee_list(request):
    committees_h = Committee.objects.filter(chamber='H').select_related()
    committees_s = Committee.objects.filter(chamber="S").select_related()

    context = {
        'committees': {
            'house': committees_h,
            'senate': committees_s,
        },
    }

    return render(request, "committees/committee_list.html", context)

def committee_detail(request, slug):
    committee = get_object_or_404(Committee, slug=slug)
    context = {
        'committee': committee,
    }
    return render(request, "committees/committee_detail.html", context)

def hearing_list(request):
    hearing_list = Hearing.objects.all()
    paginator = Paginator(hearing_list, settings.PAGINATE)
    page = request.GET.get('page', 1)
    try:
        hearings = paginator.page(page)
    except InvalidPage:
        raise Http404

    context = {
        'page': hearings,
    }

    return render(request, "committees/hearing_list.html", context)

def hearing_detail(request, slug):
    hearing = get_object_or_404(Hearing, slug=slug)
    # photos = [p.get_size(300, 199) for p in hearing.photos.all()] # force resize
    photos = Size.objects.filter(photo__hearing=hearing, width=300, height=199).select_related()
    context = {
        'hearing': hearing,
        'photos': photos,
    }
    return render(request, "committees/hearing_detail.html", context)