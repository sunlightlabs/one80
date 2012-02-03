import datetime
from itertools import chain
from haystack.indexes import *
from haystack import site
from one80.committees.models import Committee, Hearing


class CommitteeIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    result_type = CharField(faceted=True)
    name = CharField(model_attr='name')
    chamber = CharField(model_attr='chamber')
    # hearings = MultiValueField()

    def prepare_result_type(self, obj):
        return obj._meta.verbose_name_plural.lower()

    def prepare_hearings(self, obj):
        return [hearing for hearing in obj.hearings.published()]

    def index_queryset(self):
        return Committee.objects.all()


class HearingIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    result_type = CharField(faceted=True)
    name = CharField(model_attr='title')
    summary = CharField(model_attr='description')
    date = DateTimeField(model_attr='start_datetime')
    location = CharField(model_attr='location')
    # committee = CharField(model_attr='committee')
    # people = MultiValueField()

    def prepare_result_type(self, obj):
        return obj._meta.verbose_name_plural.lower()

    def prepare_people(self, obj):
        return [annotation.name for annotation in chain.from_iterable([
                    photo.annotations.published() for photo in obj.photos.all()
                    ])]

    def index_queryset(self):
        return Hearing.objects.published()

site.register(Committee, CommitteeIndex)
site.register(Hearing, HearingIndex)