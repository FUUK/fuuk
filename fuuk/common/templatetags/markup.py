"""
Filters which transform plain text to HTML.
"""
import markdown as _markdown
import textile as _textile
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def textile(value):
    """
    Returns HTML create by Textile markup language.
    """
    return mark_safe(_textile.textile(value))


@register.filter
@stringfilter
def markdown(value):
    """
    Returns HTML created by markdown language.
    """
    return mark_safe(_markdown.markdown(value))
