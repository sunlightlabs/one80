from django.db import models

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
        return [chamber[1] for chamber in CHAMBERS if chamber[0] == self.chamber][0]

class HearingManager(models.Manager):
    use_for_related_fields = True

    def published(qset, user=None):
        try:
            if user.is_staff:
                return qset.all()
        except AttributeError:
            pass

        qset = qset.filter(is_public=True)
        return qset

class Hearing(models.Model):
    committee = models.ForeignKey(Committee, related_name="hearings")
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    start_datetime = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=128, blank=True)
    is_public = models.BooleanField(default=False)

    objects = HearingManager()

    class Meta:
        ordering = ('-start_datetime',)

    def __unicode__(self):
        return self.title

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
