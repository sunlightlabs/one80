import cStringIO
import datetime
import json
import os

from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.db import models
from django.db.models.signals import pre_save
from django.template import Context
from django.template.loader import get_template
from PIL import Image

from one80.committees.models import Hearing
from one80.people.models import Person

EXTENSIONS = ((x, x) for x in ('jpg',))

def resize_path(instance, filename):
    filename = "%s-%sx%s.%s" % (instance.photo.name, instance.width, instance.height, instance.photo.extension)
    return os.path.join(instance.photo.hearing.slug, filename)

def annotation_thumbnail_path(instance, filename):
    original = instance.photo.sizes.filter(is_original=True)[0]
    filename = "%s-%s-at-%s-%sx%s.%s" % (instance.first_name, instance.last_name, instance.photo.name,
                                         instance.width(original.width), instance.height(original.height),
                                         instance.photo.extension)
    filename = filename.lower()
    return os.path.join(instance.photo.hearing.slug, 'annotations', filename)

class Photo(models.Model):
    hearing = models.ForeignKey(Hearing, related_name="photos")
    name = models.CharField(max_length=128)
    extension = models.CharField(max_length=4, choices=EXTENSIONS)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    def get_filename(self):
        return "%s.%s" % (self.name, self.extension)

    def get_size(self, width, height=None):

        if height is None:
            original = self.sizes.filter(is_original=True)[0]
            height = (width * original.height) / original.width

        try:
            size = self.sizes.get(width=width, height=height)
        except Size.DoesNotExist:
            size = self.resize(width, height)

        return size

    def resize(self, width, height):

        original = self.sizes.filter(is_original=True)[0]

        bffr = cStringIO.StringIO()

        img = Image.open(original.image.path)
        img = img.resize((width, height), Image.ANTIALIAS)
        img.save(bffr, "JPEG")

        resized = Size(photo=self, width=width, height=height)
        resized.image.save(self.get_filename(), ContentFile(bffr.getvalue()))

        bffr.close()

        return resized

class Size(models.Model):
    photo = models.ForeignKey(Photo, related_name='sizes')
    width = models.IntegerField(blank=True)
    height = models.IntegerField(blank=True)
    image = models.ImageField(upload_to=resize_path, height_field='height', width_field='width')
    is_original = models.BooleanField(default=False)

    def __unicode__(self):
        return u"%sx%s" % (self.width, self.height)

    def create_annotation(self, x, y, width, height, **kwargs):

        user = kwargs['user']
        dims = self.size_annotation(x, y, width, height)
        params = {
            'photo': self.photo,
            'created_by': user,
            'x_pct': dims[0],
            'y_pct': dims[1],
            'width_pct': dims[2],
            'height_pct': dims[3],
        }

        return Annotation(**params)

    def size_annotation(self, x, y, width, height):

        img_width = float(self.width)
        img_height = float(self.height)

        return (
            x / img_width,
            y / img_height,
            width / img_width,
            height / img_height,
        )

    @property
    def annotations(self):

        annots = []
        for annot in self.photo.annotations.published():
            annots.append(annot.to_dict(self.width, self.height))

        return annots

    def annotations_as_user(self, user):
        annots = []
        for annot in self.photo.annotations.published(user):
            annots.append(annot.to_dict(self.width, self.height, user))

        return annots


class AnnotationManager(models.Manager):
    use_for_related_fields = True

    def published(qset, user=None):
        try:
            if user.is_staff:
                return qset.all()
        except AttributeError:
            pass

        original_qset = qset
        qset = qset.filter(is_public=True)
        if user and user.id:
            qset |= original_qset.filter(is_public=False, created_by=user)

        return qset.order_by('-published_date')

    def unpublished(qset, user=None):
        return qset.filter(is_public=False)

class Annotation(models.Model):
    photo = models.ForeignKey(Photo, related_name='annotations')
    created_by = models.ForeignKey(User, related_name='annotations')
    is_public = models.BooleanField(default=False)
    x_pct = models.FloatField()
    y_pct = models.FloatField()
    width_pct = models.FloatField()
    height_pct = models.FloatField()
    thumbnail = models.ImageField(upload_to=annotation_thumbnail_path, blank=True, null=True)

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    organization = models.CharField(max_length=128, blank=True)
    title = models.CharField(max_length=255, blank=True)
    url = models.URLField(verify_exists=True, blank=True)

    person = models.ForeignKey(Person, related_name='annotations', blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add = True)
    published_date = models.DateTimeField(blank=True, null=True)

    objects = AnnotationManager()

    class Meta:
        ordering = ('-created_date',)

    def __unicode__(self):
        return "%s %s - %s" % (self.first_name,
                               self.last_name,
                               self.title + ', ' + self.organization if self.title else self.organization)

    def save(self, *args, **kwargs):
        ''' ensure timestamp on publish and generate thumbnail '''
        if self.is_public and not self.published_date:
            self.published_date = datetime.datetime.now()
        try:
            self.thumbnail.delete(save=False)
        except:
            pass
        if self.is_public:
            self._get_thumbnail()

        super(Annotation, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        ''' clean up thumbnails on delete '''
        super(Annotation, self).delete(*args, **kwargs)
        try:
            self.thumbnail.delete(save=False)
        except:
            pass

    @property
    def name(self):
        return "%s %s" % (self.first_name, self.last_name)

    @property
    def position(self):
        return "%s%s" % (self.title + ', ' if self.title else '', self.organization)

    @property
    def hearing(self):
        return self.photo.hearing


    def area(self, img_width, img_height):

        x = int(round(img_width * self.x_pct))
        y = int(round(img_height * self.y_pct))
        width = int(round(img_width * self.width_pct))
        height = int(round(img_height * self.height_pct))

        return "%s,%s,%s,%s" % (x, y, x + width, y + height)

    def coords(self, img_width, img_height):

        x = int(round(img_width * self.x_pct))
        y = int(round(img_height * self.y_pct))
        width = self.width(img_width)
        height = self.height(img_height)

        return (
            (x, y),
            (x + width, y),
            (x + width, y + height),
            (x, y + height),
        )

    def width(self, img_width):
        return int(round(img_width * self.width_pct))

    def height(self, img_height):
        return int(round(img_height * self.height_pct))

    def is_editable_by(self, user=None):
        if not user:
            return False

        if user.is_superuser:
            return True

        if (user.id == self.created_by.id and not self.is_public):
            return True

        return False

    def get_filename(self):
        return "%s-%s-%s.%s" % (self.photo.name, self.first_name, self.last_name, self.photo.extension)

    def to_dict(self, img_width, img_height, user=None):
        coord_sets = self.coords(img_width, img_height)
        left = coord_sets[0][0]
        top = coord_sets[0][1]
        width = coord_sets[2][0] - left
        height = coord_sets[2][1] - top
        data = {
            'left': left,
            'top': top,
            'width': width,
            'height': height,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'display_name': self.name,
            'position': self.position,
            'title': self.title,
            'organization': self.organization,
            'url': self.url,
            'id': self.id,
            'is_public': self.is_public,
            'editable': self.is_editable_by(user),
        }
        if self.is_public:
            try:
                person = self.person
                data.update({
                    'first_name': person.first_name,
                    'last_name': person.last_name,
                    'title': person.title,
                    'organization': person.organization,
                    'display_name': person.name,
                    'position': person.position,
                    'url': person.url,
                })
            except:
                pass

        return data

    def _get_thumbnail(self, **kwargs):
        original = self.photo.sizes.filter(is_original=True)[0]
        coords = self.coords(original.width, original.height)

        bffr = cStringIO.StringIO()

        img = Image.open(original.image.path).copy()
        img = img.crop((coords[0][0], coords[0][1], coords[2][0], coords[2][1]))
        img.save(bffr, "JPEG")

        self.thumbnail.save(self.get_filename(), ContentFile(bffr.getvalue()), save=False)
        bffr.close()

def save_annotation_handler(sender, instance, *args, **kwargs):
    if instance.is_public and not instance.person:
        instance.person = Person.objects.get_or_create(first_name=instance.first_name,
                                                       last_name=instance.last_name,
                                                       title=instance.title,
                                                       organization=instance.organization,)[0]

pre_save.connect(save_annotation_handler, sender=Annotation)