from modeltranslation.translator import register, TranslationOptions

from fuuk.people.models import News


@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'content')
