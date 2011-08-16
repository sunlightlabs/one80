from django.contrib import admin
from one80.photos.models import Photo, Size, Annotation

class AnnotationInline(admin.StackedInline):
    model = Annotation
    extra = 0

class SizeInline(admin.TabularInline):
    model = Size
    extra = 0

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('name', 'hearing')
    list_filter = ('hearing',)
    inlines = (SizeInline, AnnotationInline)

admin.site.register(Photo, PhotoAdmin)
#admin.site.register(Size)
#admin.site.register(Annotation)