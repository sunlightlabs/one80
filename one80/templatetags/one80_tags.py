from django import template
from django.utils.safestring import mark_safe
from django.template.base import TemplateSyntaxError


register = template.Library()

@register.filter
def link_if(string, url):
    if url:
        return mark_safe('<a href="%s" target="_blank">%s</a>' % (url, string))
    else:
        return string

@register.filter
def subtract(val, diff):
    try:
        return int(float(val) - float(diff))
    except:
        return val


# def url_for(parser, token):
#     bits = token.split_contents()
#     if len(bits) < 2:
#         raise TemplateSyntaxError("'%s' takes at least one argument"
#                                   " (path to a view)" % bits[0])
#     viewname = bits[1]
#     args = []
#     kwargs = {}
#     asvar = None
#     bits = bits[2:]
#     if len(bits) >= 2 and bits[-2] == 'as':
#         asvar = bits[-1]
#         bits = bits[:-2]

#     if len(bits):
#     for bit in bits:
#         match = kwarg_re.match(bit)
#         if not match:
#             raise TemplateSyntaxError("Malformed arguments to url tag")
#         name, value = match.groups()
#         if name:
#             kwargs[name] = parser.compile_filter(value)
#         else:
#             args.append(parser.compile_filter(value))

#     return URLNode(viewname, args, kwargs, asvar, legacy_view_name=True)
