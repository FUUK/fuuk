from django.contrib.flatpages.models import FlatPage
from modeltranslation.translator import register, TranslationOptions


@register(FlatPage)
class FlatPageTranslationOptions(TranslationOptions):
    fields = ('title', 'content')
