from django import template
from django.utils.safestring import mark_safe


register = template.Library()

@register.filter
def link_if(string, url):
    if url:
        return mark_safe('<a href="%s" target="_blank">%s</a>' % (url, string))
    else:
        return string