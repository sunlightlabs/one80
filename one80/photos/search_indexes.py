import datetime
from haystack.indexes import *
from haystack import site
from one80.photos.models import Photo, Annotation


class AnnotationIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)
    result_type = CharField(faceted=True)
    desc = CharField(faceted=True)
    name = CharField(model_attr='name')
    position = CharField(model_attr='position')
    hearing = CharField(model_attr='hearing')
    date = DateTimeField(model_attr='published_date', null=True)

    def prepare_result_type(self, obj):
        return obj._meta.verbose_name_plural.lower()

    def prepare_desc(self, obj):
        return "%s %s %s" % (obj.name, obj.title, obj.organization)

    def index_queryset(self):
        return Annotation.objects.published()

site.register(Annotation, AnnotationIndex)