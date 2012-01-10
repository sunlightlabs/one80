from django.contrib import admin
from one80.committees.models import Committee, Hearing

class HearingAdmin(admin.ModelAdmin):
    list_display = ('title','start_datetime','is_public')
    list_filter = ('is_public',)
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Committee)
admin.site.register(Hearing, HearingAdmin)