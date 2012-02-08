from django.contrib import admin
from one80.committees.models import Committee, Hearing

class CommitteeAdmin(admin.ModelAdmin):
    list_display = ('name', 'chamber',)
    list_filter = ('chamber',)
    prepopulated_fields = {'slug': ('name',)}

class HearingAdmin(admin.ModelAdmin):
    list_display = ('title','start_datetime','is_public',)
    list_filter = ('is_public', 'committee__name', 'committee__chamber',)
    date_hierarchy = 'start_datetime'
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Committee, CommitteeAdmin)
admin.site.register(Hearing, HearingAdmin)