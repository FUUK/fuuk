# coding: utf-8
from django.contrib import admin

import multilingual
from people.models import Department, Place, Human, Person, Course, Attachment, Grant, Article, Author, Thesis

class DepartmentAdmin(multilingual.MultilingualModelAdmin):
    list_display = ('name', 'fax')

class PlaceAdmin(multilingual.MultilingualModelAdmin):
    list_display = ('name', 'phone', 'department')

class HumanAdmin(admin.ModelAdmin):
    list_display = ('nickname',)

class PersonAdmin(multilingual.MultilingualModelAdmin):
    list_display = ('human', 'type', 'first_name', 'last_name', 'place')

class CourseAdmin(multilingual.MultilingualModelAdmin):
    list_display = ('name', 'ls', 'zs', 'code')

class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('course', 'title')

class GrantAdmin(multilingual.MultilingualModelAdmin):
    list_display = ('author', 'number', 'title', 'start', 'end')

class ArticleAdmin(multilingual.MultilingualModelAdmin):
    list_display = ('title', 'type', 'year')

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('person', 'article', 'order')

class ThesisAdmin(multilingual.MultilingualModelAdmin):
    list_display = ('type', 'title', 'author', 'advisor')

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

