# coding: utf-8
from django.contrib import admin
import multilingual
from people.models.place import Department, Place
from people.models.person import Human, Person

from people.models.course import Course, Attachment
from people.models.grant import Grant
from people.models.article import Article, Author
from people.models.thesis import Thesis

class PlaceAdmin(multilingual.MultilingualModelAdmin):
    list_display = ('name', 'phone', 'department')

admin.site.register( Place, PlaceAdmin)

class DepartmentAdmin(multilingual.MultilingualModelAdmin):
    list_display = ('name', 'fax')

admin.site.register( Department, DepartmentAdmin)

class PersonAdmin(multilingual.MultilingualModelAdmin):
    list_display = ('human', 'type', 'first_name', 'last_name', 'place')

admin.site.register( Person, PersonAdmin)

class ThesisAdmin(multilingual.MultilingualModelAdmin):
    list_display = ('type', 'title', 'author', 'advisor')

admin.site.register( Thesis, ThesisAdmin)

class CourseAdmin(multilingual.MultilingualModelAdmin):
    list_display = ('name', 'ls', 'zs', 'code')

admin.site.register( Course, CourseAdmin)

class HumanAdmin(admin.ModelAdmin):
    list_display = ('nickname',)

admin.site.register( Human, HumanAdmin)

class GrantAdmin(multilingual.MultilingualModelAdmin):
    list_display = ('author', 'number', 'title', 'start', 'end')

admin.site.register( Grant, GrantAdmin)

