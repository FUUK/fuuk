"""
Filters which transform plain text to HTML.
"""
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from markdownx.utils import markdownify

register = template.Library()


@register.filter
@stringfilter
def markdown(value):
    """
    Returns HTML created by markdown language.
    """
    # Use the `markdownify` from `markdownx` to get the same results.
    return mark_safe(markdownify(value))
