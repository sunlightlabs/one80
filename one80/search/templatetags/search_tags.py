from django import template

register = template.Library()

@register.filter
def search_display_name(string):
    names = {
        'annotations': 'tags',
        'people': 'attendees',
    }
    return names.get(string, string)