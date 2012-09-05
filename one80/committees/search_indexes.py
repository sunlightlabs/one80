from itertools import chain
from haystack.indexes import *
from haystack import site
from one80.committees.models import Committee, Hearing


class CommitteeIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)
    result_type = CharField(faceted=True)
    name = CharField(model_attr='name')
    slug = CharField(model_attr='slug')
    chamber = CharField(model_attr='chamber')
    # hearings = MultiValueField()

    def prepare_result_type(self, obj):
        return obj._meta.verbose_name_plural.lower()

    def prepare_hearings(self, obj):
        return [hearing for hearing in obj.hearings.published()]

    def index_queryset(self):
        return Committee.objects.all()

site.register(Committee, CommitteeIndex)


class HearingIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)
    result_type = CharField(faceted=True)
    name = CharField(model_attr='title')
    slug = CharField(model_attr='slug')
    summary = CharField(model_attr='description')
    date = DateTimeField(model_attr='start_datetime')
    location = CharField(model_attr='location')
    is_parent = BooleanField(default='')
    is_public = BooleanField(default='')
    # committee = CharField(model_attr='committee')
    # people = MultiValueField()

    def prepare_result_type(self, obj):
        return obj._meta.verbose_name_plural.lower()

    def prepare_is_parent(self, obj):
        return ''

    def prepare_is_public(self, obj):
        if obj.is_public:
            return True
        return ''

    def prepare_people(self, obj):
        return [annotation.name for annotation in chain.from_iterable([
                    photo.annotations.published() for photo in obj.photos.all()
                    ])]

    def index_queryset(self):
        return Hearing.objects.published()

site.register(Hearing, HearingIndex)
