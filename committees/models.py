from django.db import models

CHAMBERS = (
    ('H', 'House of Representatives'),
    ('S', 'Senate'),
)

class Committee(models.Model):
    name = models.CharField(max_length=255)
    chamber = models.CharField(max_length=1, choices=CHAMBERS)
    
    class Meta:
        ordering = ('name',)
    
    def __unicode__(self):
        return self.name

class Hearing(models.Model):
    committee = models.ForeignKey(Committee, related_name="hearings")
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True)
    start_datetime = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=128, blank=True)
    is_public = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('-start_datetime',)
    
    def __unicode__(self):
        return self.title