from modeltranslation.translator import register, TranslationOptions

from fuuk.people.models import Department, News, Place


@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'content')


@register(Department)
class DepartmentTranslationOptions(TranslationOptions):
    fields = ('name', )


@register(Place)
class PlaceTranslationOptions(TranslationOptions):
    fields = ('name', )
