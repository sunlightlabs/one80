import json

from django.db import models
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify
from jsonfield.fields import JSONField

class Person(models.Model):
    slug = models.SlugField(max_length=50)
    first_name = models.CharField(max_length=50, blank=True, default='')
    middle_name = models.CharField(max_length=50, blank=True, default='')
    last_name = models.CharField(max_length=50, blank=True, default='')
    organization = models.CharField(max_length=255, blank=True, default='')
    title = models.CharField(max_length=50, blank=True, default='')
    url = models.URLField(verify_exists=False, blank=True, default='')
    extra = JSONField(blank=True, default='{}', help_text='JSON string of extra data key/value pairs')

    class Meta:
        verbose_name_plural = 'people'

    def __unicode__(self):
        return "%s, %s - %s at %s" % (self.last_name, self.first_name, self.title, self.organization)

    @property
    def name(self):
        return "%s %s" % (self.first_name, self.last_name)

    @property
    def position(self):
        return "%s%s" % (self.title + ', ' if self.title else '', self.organization)

def ensure_unique_slug(sender, *args, **kwargs):
    instance = kwargs['instance']
    klass = instance.__class__
    slugs = [sl.values()[0] for sl in klass.objects.values('slug')]
    if not instance.slug:
        slug = slugify(instance.name)[:45]
        if slug in slugs:
            import re
            counterFinder = re.compile(r'-\d+$')
            counter = 2
            slug = '%s-%i' % (slug, counter)
            while slug in slugs:
                slug = re.sub(counterFinder, '-%i' % counter, slug)
                counter += 1

        instance.slug = slug

pre_save.connect(ensure_unique_slug, sender=Person)

###############################
## South Introspection Rules ##
###############################
try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^jsonfield\.fields\.JSONField"])
except:
    pass