from django.contrib import admin
from one80.auth.models import UserProfile
from one80.auth.forms import UserProfileForm, UserProfileAdminForm

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'phone', 'provider', 'is_complete')
    list_filter = ('is_complete',)
    readonly_fields = ('is_complete',)
    form = UserProfileAdminForm

admin.site.register(UserProfile, UserProfileAdmin)