from django import template

register = template.Library()

@register.simple_tag
def getsize(photo, width, height):
    size = photo.get_size(width, height)
    return size.image.url