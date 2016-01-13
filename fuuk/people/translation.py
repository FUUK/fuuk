from modeltranslation.translator import register, TranslationOptions

from fuuk.people.models import Course, Department, Human, News, Place


@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'content')


@register(Department)
class DepartmentTranslationOptions(TranslationOptions):
    fields = ('name', )


@register(Place)
class PlaceTranslationOptions(TranslationOptions):
    fields = ('name', )


@register(Course)
class CourseTranslationOptions(TranslationOptions):
    fields = ('name', 'annotation', 'note')


@register(Human)
class HumanTranslationOptions(TranslationOptions):
    fields = ('subtitle', 'cv', 'interests', 'stays')
