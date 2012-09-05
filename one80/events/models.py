from django.db import models
from django.contrib.contenttypes import generic

from one80.photos.models import Photo


class EventManager(models.Manager):
    use_for_related_fields = True

    def published(qset, user=None):
        try:
            if user.is_staff:
                return qset.all()
        except AttributeError:
            pass

        qset = qset.filter(is_public=True)
        return qset

    def with_children(qset):
        return qset.filter(child_events__isnull=False)

    def published_with_children(qset, user=None):
        try:
            if user.is_staff:
                return qset.filter(child_events__isnull=False)
        except AttributeError:
            pass

        qset = qset.filter(is_public=True).filter(child_events__isnull=False)
        return qset

    def children(qset):
        return qset.filter(parent_event_id__isnull=False)

    def published_children(qset, user=None):
        try:
            if user.is_staff:
                return qset.filter(parent_event_id__isnull=False)
        except AttributeError:
            pass

        qset = qset.filter(is_public=True).filter(parent_event_id__isnull=False)
        return qset


class AbstractEvent(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    start_datetime = models.DateTimeField()
    location = models.CharField(max_length=128, blank=True)
    is_public = models.BooleanField(default=False)
    photos = generic.GenericRelation(Photo)

    objects = EventManager()

    class Meta:
        abstract = True
        ordering = ('-start_datetime',)

    def __unicode__(self):
        return self.title

    @property
    def object_type(self):
        return self._meta.verbose_name

    @property
    def object_type_plural(self):
        return self._meta.verbose_name_plural

    @property
    def annotated_names(self):
        try:
            return self._annotated_names
        except AttributeError:
            self._annotated_names = []
            for photo in self.photos.all():
                for annot in photo.annotations.published():
                    if annot.name not in self._annotated_names:
                        self._annotated_names.append(annot.name)

        return self._annotated_names

    @property
    def annotated_names_with_urls(self):
        try:
            return self._annotated_names_with_urls
        except AttributeError:
            self._annotated_names_with_urls = []
            names = []
            for photo in self.photos.all():
                for annot in photo.annotations.published():
                    if annot.name not in names:
                        names.append(annot.name)
                        self._annotated_names_with_urls.append((annot.name, annot.url))

        return self._annotated_names_with_urls


class PublicEventManager(EventManager):
    pass


class PublicEvent(AbstractEvent):
    parent_event = models.ForeignKey('PublicEvent', related_name="child_events", blank=True, null=True)

    objects = PublicEventManager()

    class Meta(AbstractEvent.Meta):
        db_table = 'events_event'
