from django.db import models
from one80.events.models import AbstractEvent, EventManager
# from one80.photos.models import Annotation

CHAMBERS = (
    ('H', 'House of Representatives'),
    ('S', 'Senate'),
)


class Committee(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    chamber = models.CharField(max_length=1, choices=CHAMBERS)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    @property
    def chamber_name(self):
        return self.get_chamber_display()


class HearingManager(EventManager):
    pass


class Hearing(AbstractEvent):
    committee = models.ForeignKey(Committee, related_name="hearings")

    objects = HearingManager()

    class Meta(AbstractEvent.Meta):
        db_table = 'committees_hearing'
