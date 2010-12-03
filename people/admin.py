# coding: utf-8
from django.contrib import admin

import multilingual
from people.models import Department, Place, Human, Person, Course, Attachment, Grant, Article, Author, Thesis

class DepartmentAdmin(multilingual.MultilingualModelAdmin):
    list_display = ('name', 'fax')

class PlaceAdmin(multilingual.MultilingualModelAdmin):
    list_display = ('name', 'phone', 'department')

class HumanAdmin(multilingual.MultilingualModelAdmin):
    list_display = ('nickname', 'email', 'birth_date', 'birth_place')
    ordering = ('nickname',)

class PersonAdmin(admin.ModelAdmin):
    list_display = ('human', 'type', 'first_name', 'last_name', 'place')
    list_filter = ('type',)
    ordering = ('last_name',)

class CourseAdmin(multilingual.MultilingualModelAdmin):
    list_display = ('name', 'ls', 'zs', 'code')
    filter_horizontal = ('lectors',)

class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('course', 'title')

class GrantAdmin(multilingual.MultilingualModelAdmin):
    list_display = ('author', 'number', 'title', 'start', 'end')
    filter_horizontal = ('co_authors',)

class ArticleAdmin(multilingual.MultilingualModelAdmin):
    list_display = ('title', 'type', 'year')
    list_filter = ('type', 'year')

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('person', 'article', 'order')
    list_filter = ('article',)

class ThesisAdmin(multilingual.MultilingualModelAdmin):
    list_display = ('type', 'title', 'author', 'advisor')
    filter_horizontal = ('consultants',)

admin.site.register(Place, PlaceAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Human, HumanAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Attachment, AttachmentAdmin)
admin.site.register(Grant, GrantAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Thesis, ThesisAdmin)
