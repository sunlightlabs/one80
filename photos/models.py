from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.db import models
from one80.committees.models import Hearing
from PIL import Image
import os
import cStringIO

EXTENSIONS = ((x, x) for x in ('jpg',))

def resize_path(instance, filename):
    filename = "%s-%sx%s.%s" % (instance.photo.name, instance.width, instance.height, instance.photo.extension)
    return os.path.join(instance.photo.hearing.slug, filename)

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

    def create_annotation(self, x, y, width, height):

        img_width = float(self.width)
        img_height = float(self.height)
        
        params = {
            'photo': self.photo,
            'x_pct': x / img_width,
            'y_pct': y / img_height,
            'width_pct': width / img_width,
            'height_pct': height / img_height,
        }

        return Annotation(**params)
    
    def annotations(self):
        
        annots = []
        for annot in self.photo.annotations.all():
            annots.append({
                'created_by': annot.created_by,
                'coordinates': annot.coords(self.width, self.height),
                'area': annot.area(self.width, self.height),
                'first_name': annot.first_name,
                'last_name': annot.last_name,
                'organization': annot.organization,
                'title': annot.title,
            })
        
        return annots

class Annotation(models.Model):
    photo = models.ForeignKey(Photo, related_name='annotations')
    created_by = models.ForeignKey(User, related_name='annotations')
    x_pct = models.FloatField()
    y_pct = models.FloatField()
    width_pct = models.FloatField()
    height_pct = models.FloatField()
    
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    organization = models.CharField(max_length=128, blank=True)
    title = models.CharField(max_length=128, blank=True)
    
    def coords(self, img_width, img_height):
        
        x = int(round(img_width * self.x_pct))
        y = int(round(img_height * self.y_pct))
        width = int(round(img_width * self.width_pct))
        height = int(round(img_height * self.height_pct))
        
        return (
            (x, y),
            (x + width, y),
            (x + width, y + height),
            (x, y + height),
        )
    
    def area(self, img_width, img_height):
        
        x = int(round(img_width * self.x_pct))
        y = int(round(img_height * self.y_pct))
        width = int(round(img_width * self.width_pct))
        height = int(round(img_height * self.height_pct))
        
        return "%s,%s,%s,%s" % (x, y, x + width, y + height)