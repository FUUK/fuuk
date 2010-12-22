# coding: utf-8
from django.contrib import admin
from django.db import models
from django.forms import CharField

import multilingual
from people.admin.forms import ArticleBookForm, ArticleArticleForm, ArticleTalkForm, ArticlePosterForm
from people.models import Department, Place, Human, Person, Course, Attachment, Grant, Article, Author, Thesis


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
    list_display = ('human', 'type', 'first_name', 'last_name', 'place')
    list_filter = ('type',)
    ordering = ('last_name',)
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


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'year')
    list_filter = ('type', 'year')
    formfield_overrides = {
        models.CharField: {'form_class': NullCharField},
    }


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('person', 'article', 'order')
    list_filter = ('article',)


class ThesisAdmin(multilingual.MultilingualModelAdmin):
    list_display = ('type', 'title', 'author', 'advisor')
    filter_horizontal = ('consultants',)
    formfield_overrides = {
        models.CharField: {'form_class': NullCharField},
    }


### Articles

class ArticleBookAdmin(ArticleAdmin):
    form = ArticleBookForm

    def queryset(self, request):
        return super(ArticleBookAdmin, self).queryset(request).filter(type='BOOK')


class ArticleArticleAdmin(ArticleAdmin):
    form = ArticleArticleForm

    def queryset(self, request):
        return super(ArticleArticleAdmin, self).queryset(request).filter(type='ARTICLE')


class ArticleTalkAdmin(ArticleAdmin):
    form = ArticleTalkForm

    def queryset(self, request):
        return super(ArticleTalkAdmin, self).queryset(request).filter(type='TALK')


class ArticlePosterAdmin(ArticleAdmin):
    form = ArticlePosterForm

    def queryset(self, request):
        return super(ArticlePosterAdmin, self).queryset(request).filter(type='POSTER')
