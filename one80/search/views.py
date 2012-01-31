from django.conf import settings
from django.core.paginator import Paginator, InvalidPage
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from haystack import site
from haystack.forms import ModelSearchForm, EmptySearchQuerySet
from haystack.query import SearchQuerySet


RESULTS_PER_PAGE = getattr(settings, 'HAYSTACK_SEARCH_RESULTS_PER_PAGE', 20)

def search(request, template='search/search.html', load_all=True,
                          form_class=ModelSearchForm, searchqueryset=None,
                          context_class=RequestContext, extra_context=None, results_per_page=5):
    query = ''
    results = EmptySearchQuerySet()

    if request.GET.get('q'):
        form = form_class(request.GET, searchqueryset=searchqueryset, load_all=load_all)

        if form.is_valid():
            query = form.cleaned_data['q']
            results = form.search()
    else:
        form = form_class(searchqueryset=searchqueryset, load_all=load_all)

    # only get faceted results if there were matches
    facet_results = {}
    if results:
        facet_counts = results.facet_counts()['fields']['result_type']
        for result_type in facet_counts:
            if result_type[1] > 0:
                facet_results[result_type[0]] = {
                    'count': result_type[1],
                    'objects': SearchQuerySet().filter(content=query,
                                                       result_type__exact=result_type[0])[:int(results_per_page)],
                }

    context = {
        'form': form,
        'facet_results': facet_results,
        'query': query,
        'suggestion': None,
    }

    if getattr(settings, 'HAYSTACK_INCLUDE_SPELLING', False):
            context['suggestion'] = form.get_suggestion()

    if extra_context:
        context.update(extra_context)

    return render_to_response(template, context, context_instance=context_class(request))

def narrowed_search(request, template='search/narrowed_search.html', load_all=True,
                        form_class=ModelSearchForm, searchqueryset=None,
                        context_class=RequestContext, extra_context=None, results_per_page=RESULTS_PER_PAGE, **kwargs):

    query = ''
    result_type = kwargs.get('result_type')
    results = EmptySearchQuerySet()

    # ensure a valid facet
    if result_type not in [model._meta.verbose_name_plural.lower() for model in site.get_indexes().keys()]:
        raise Http404

    if request.GET.get('q'):
        form = form_class(request.GET, searchqueryset=searchqueryset.filter(result_type__exact=result_type), load_all=load_all)

        if form.is_valid():
            query = form.cleaned_data['q']
            results = form.search()
    else:
        form = form_class(searchqueryset=searchqueryset, load_all=load_all)

    paginator = Paginator(results, results_per_page)

    try:
        page = paginator.page(int(request.GET.get('page', 1)))
    except InvalidPage:
        raise(Http404('No such page of results!'))

    context = {
        'form': form,
        'page': page,
        'paginator': paginator,
        'result_type': result_type,
        'query': query,
        'suggestion': None
    }

    if getattr(settings, 'HAYSTACK_INCLUDE_SPELLING', False):
            context['suggestion'] = form.get_suggestion()

    if extra_context:
        context.update(extra_context)

    return render_to_response(template, context, context_instance=context_class(request))
