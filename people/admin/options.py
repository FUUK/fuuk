# coding: utf-8
from django.contrib import admin
from django.db import models

import multilingual
from people.admin.fields import NullCharField
from people.admin.forms import ArticleBookForm, ArticleArticleForm, ArticleConferenceForm
from people.models import Attachment, Author


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


class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('course', 'title')


class AttachmentInlineAdmin(admin.TabularInline):
    model = Attachment
    extra = 3


class CourseAdmin(multilingual.MultilingualModelAdmin):
    list_display = ('name', 'ls', 'zs', 'code')
    inlines = [AttachmentInlineAdmin, ]
    filter_horizontal = ('lectors',)
    ordering = ('code',)
    formfield_overrides = {
        models.CharField: {'form_class': NullCharField},
    }


class GrantAdmin(multilingual.MultilingualModelAdmin):
    list_display = ('author', 'number', 'title', 'start', 'end')
    filter_horizontal = ('co_authors',)


class ThesisAdmin(multilingual.MultilingualModelAdmin):
    list_display = ('type', 'title', 'author', 'advisor')
    filter_horizontal = ('consultants',)
    list_filter = ('type', 'year')
    formfield_overrides = {
        models.CharField: {'form_class': NullCharField},
    }


class AuthorInlineAdmin(admin.TabularInline):
    model = Author
    extra = 3
    fields = ('order', 'person')
    readonly_fields = ('order',)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        defaults = {
            'queryset': db_field.rel.to.objects.order_by('last_name', 'first_name')
        }
        defaults.update(kwargs)
        return super(AuthorInlineAdmin, self).formfield_for_foreignkey(db_field, request, **defaults)

    def queryset(self, request):
        # Return ordered authors
        return super(AuthorInlineAdmin, self).queryset(request).order_by('order')

### Articles
class BaseArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'year')
    list_filter = ('year',)
    inlines = [AuthorInlineAdmin, ]
    formfield_overrides = {
        models.CharField: {'form_class': NullCharField},
    }


class ArticleAdmin(BaseArticleAdmin):
    list_filter = ('type', 'year')


class ArticleBookAdmin(BaseArticleAdmin):
    form = ArticleBookForm

    def queryset(self, request):
        return super(ArticleBookAdmin, self).queryset(request).filter(type='BOOK')


class ArticleArticleAdmin(BaseArticleAdmin):
    form = ArticleArticleForm

    def queryset(self, request):
        return super(ArticleArticleAdmin, self).queryset(request).filter(type='ARTICLE')


class ArticleConferenceAdmin(BaseArticleAdmin):
    form = ArticleConferenceForm

    def queryset(self, request):
        return super(ArticleConferenceAdmin, self).queryset(request).filter(type__in=('TALK', 'INVITED', 'POSTER'))
