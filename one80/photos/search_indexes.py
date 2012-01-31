import datetime
from haystack.indexes import *
from haystack import site
from one80.photos.models import Photo, Annotation


class AnnotationIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    result_type = CharField(faceted=True)
    name = CharField(model_attr='name')
    position = CharField(model_attr='position')
    hearing = CharField(model_attr='hearing')
    date = DateTimeField(model_attr='published_date')

    def prepare_result_type(self, obj):
        return obj._meta.verbose_name_plural.lower()

    def index_queryset(self):
        return Annotation.objects.published()

site.register(Annotation, AnnotationIndex)