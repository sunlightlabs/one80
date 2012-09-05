from django import template
from django.core.urlresolvers import reverse, Resolver404, NoReverseMatch

register = template.Library()

@register.simple_tag
def getsize(photo, width, height):
    size = photo.get_size(width, height)
    return size.image.url

@register.simple_tag(takes_context=True)
def annotation_buttons(context, annot):
    # try:
    user = context['request'].user
    if user.is_staff:
        approve_url = reverse('annotation_approve', args=(annot.id,))
        delete_url = reverse('annotation_delete', args=(annot.id,))
        buttons = [ '<a href="%s" class="delete icon icon-remove-circle"></a>' % delete_url, ]
        if not annot.is_public:
            buttons.append('<a href="%s" class="approve icon icon-check"></a>' % approve_url)
        return ' '.join(buttons)
    # except:
    #     pass

    return ''