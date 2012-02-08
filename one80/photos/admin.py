from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe

from one80.photos.models import Photo, Size, Annotation


class AdminImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            file_name=str(value)
            output.append(u' <a style="float:left;display:block;margin-right:10px;padding:1px;border:1px solid #e9e9e9;" href="%s" target="_blank"><img src="%s" alt="%s" height="42" /></a>' % \
                (image_url, image_url, file_name))
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))

class InlineImageMixin(object):
    def formfield_for_dbfield(self, db_field, **kwargs):
            if db_field.name == 'thumbnail':
                request = kwargs.pop("request", None)
                kwargs['widget'] = AdminImageWidget
                return db_field.formfield(**kwargs)
            return super(InlineImageMixin,self).formfield_for_dbfield(db_field, **kwargs)

class AnnotationInline(InlineImageMixin, admin.StackedInline):
    model = Annotation
    extra = 0

class SizeInline(admin.TabularInline):
    model = Size
    extra = 0

class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 0

class AnnotationAdmin(InlineImageMixin, admin.ModelAdmin):
    list_display = ('__unicode__', 'photo', 'created_by')
    list_filter = ('created_by', 'is_public', 'photo')
    date_hierarchy = ('created_date')

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('name', 'hearing')
    list_filter = ('hearing__title', 'hearing__committee__name')
    inlines = (SizeInline, AnnotationInline)

admin.site.register(Photo, PhotoAdmin)
admin.site.register(Annotation, AnnotationAdmin)
#admin.site.register(Size)
