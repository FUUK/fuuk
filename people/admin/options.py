# coding: utf-8
from django.contrib import admin
from django.db import models
from django.forms import CharField

import multilingual
from people.admin.forms import ArticleBookForm, ArticleArticleForm, ArticleConferenceForm
from people.models import Person, Author


class NullCharField(CharField):
    def to_python(self, value):
        "Returns Unicode or None. postpone to save?"
        value = super(CharField, self).to_python(value)
        if value == '':
            return None
        return value


class DepartmentAdmin(multilingual.MultilingualModelAdmin):
    list_display = ('name', 'fax')
    formfield_overrides = {
        models.CharField: {'form_class': NullCharField},
    }


class PlaceAdmin(multilingual.MultilingualModelAdmin):
    list_display = ('name', 'phone', 'department')
    formfield_overrides = {
        models.CharField: {'form_class': NullCharField},
    }


class HumanAdmin(multilingual.MultilingualModelAdmin):
    list_display = ('nickname', 'email', 'birth_date', 'birth_place')
    ordering = ('nickname',)
    formfield_overrides = {
        models.CharField: {'form_class': NullCharField},
    }


class PersonAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'is_active', 'human', 'type', 'place')
    list_filter = ('type', 'is_active')
    ordering = ('human__nickname',)
    formfield_overrides = {
        models.CharField: {'form_class': NullCharField},
    }


class CourseAdmin(multilingual.MultilingualModelAdmin):
    list_display = ('name', 'ls', 'zs', 'code')
    filter_horizontal = ('lectors',)
    ordering = ('code',)
    formfield_overrides = {
        models.CharField: {'form_class': NullCharField},
    }


class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('course', 'title')


class GrantAdmin(multilingual.MultilingualModelAdmin):
    list_display = ('author', 'number', 'title', 'start', 'end')
    filter_horizontal = ('co_authors',)


class ThesisAdmin(multilingual.MultilingualModelAdmin):
    list_display = ('type', 'title', 'author', 'advisor')
    filter_horizontal = ('consultants',)
    formfield_overrides = {
        models.CharField: {'form_class': NullCharField},
    }


class AuthorInlineAdmin(admin.TabularInline):
    model = Author
    extra = 3

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        defaults = {
            'queryset': Person.objects.order_by('-is_active', 'last_name', 'first_name')
        }
        defaults.update(kwargs)
        return super(AuthorInlineAdmin, self).formfield_for_foreignkey(db_field, request, **defaults)


### Articles
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'year')
    list_filter = ('type', 'year')
    inlines = [AuthorInlineAdmin, ]
    formfield_overrides = {
        models.CharField: {'form_class': NullCharField},
    }


class ArticleBookAdmin(ArticleAdmin):
    form = ArticleBookForm

    def queryset(self, request):
        return super(ArticleBookAdmin, self).queryset(request).filter(type='BOOK')


class ArticleArticleAdmin(ArticleAdmin):
    form = ArticleArticleForm

    def queryset(self, request):
        return super(ArticleArticleAdmin, self).queryset(request).filter(type='ARTICLE')


class ArticleConferenceAdmin(ArticleAdmin):
    form = ArticleConferenceForm

    def queryset(self, request):
        return super(ArticleConferenceAdmin, self).queryset(request).filter(type__in=('TALK', 'INVITED', 'POSTER'))
