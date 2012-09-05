from haystack.query import SearchQuerySet
from django.http import Http404


def search(*args, **kwargs):
    kwargs.update(result_type__in=args)
    return SearchQuerySet().filter(**kwargs)


def search_one(*args, **kwargs):
    return search(*args, **kwargs)[0]


def search_one_or_404(*args, **kwargs):
    try:
        return search_one(*args, **kwargs)
    except IndexError:
        raise Http404
