from django.contrib import admin
from one80.events.models import PublicEvent


class PublicEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'location',)
    list_filter = ('location',)
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(PublicEvent, PublicEventAdmin)
