from django.db import models
from jsonfield.fields import JSONField

class Person(models.Model):
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

###############################
## South Introspection Rules ##
###############################
try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^jsonfield\.fields\.JSONField"])
except:
    pass