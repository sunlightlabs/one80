from django.contrib import admin

from one80.people.models import Person


class PersonAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'organization', 'title')
    list_filter = ('organization', 'title')

admin.site.register(Person, PersonAdmin)
