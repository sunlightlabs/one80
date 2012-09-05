from haystack.indexes import *
from haystack import site
from one80.people.models import Person


class PersonIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)
    result_type = CharField(faceted=True)
    desc = CharField(model_attr='desc')
    name = CharField(model_attr='name')
    slug = CharField(model_attr='slug')
    position = CharField(model_attr='position')

    def prepare_result_type(self, obj):
        return obj._meta.verbose_name_plural.lower()

    def index_queryset(self):
        return Person.objects.all()

site.register(Person, PersonIndex)
