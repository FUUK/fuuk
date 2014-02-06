"""
Filters which transform plain text to HTML.
"""
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
