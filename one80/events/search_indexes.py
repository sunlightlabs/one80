from itertools import chain
from haystack.indexes import *
from haystack import site
from one80.events.models import PublicEvent


class PublicEventIndex(RealTimeSearchIndex):
    text = CharField(document=True, use_template=True)
    result_type = CharField(faceted=True)
    name = CharField(model_attr='title')
    slug = CharField(model_attr='slug')
    summary = CharField(model_attr='description')
    date = DateTimeField(model_attr='start_datetime')
    location = CharField(model_attr='location')
    is_parent = BooleanField(default='')
    is_public = BooleanField(default='')

    def prepare_result_type(self, obj):
        return obj._meta.verbose_name_plural.lower()

    def prepare_is_parent(self, obj):
        try:
            if obj.parent_event_id is not None:
                return ''
            else:
                return True
        except AttributeError:
            return ''
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
        return PublicEvent.objects.published()

site.register(PublicEvent, PublicEventIndex)