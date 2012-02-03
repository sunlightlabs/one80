from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def unique_rank(context, text):
    try:
        current_count = context['leader'].num_tags
        prev_count = context['leaders'][context['forloop']['counter'] - 2].num_tags
        if current_count != prev_count:
            return text
        else:
            return ''
    except:
        return text
