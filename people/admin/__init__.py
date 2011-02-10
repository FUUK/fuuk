from django.contrib import admin

from people.admin.options import PlaceAdmin, DepartmentAdmin, PersonAdmin, HumanAdmin, CourseAdmin, AttachmentAdmin, \
    GrantAdmin, ThesisAdmin, AgencyAdmin, NewsAdmin, \
    ArticleAdmin, ArticleBookAdmin, ArticleArticleAdmin, ArticleConferenceAdmin
from people.models import Department, Place, Human, Person, Course, Attachment, Grant, Article, Author, Thesis, Agency, \
    ArticleBook, ArticleArticle, ArticleConference, News


admin.site.register(Place, PlaceAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Human, HumanAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Attachment, AttachmentAdmin)
admin.site.register(Grant, GrantAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Thesis, ThesisAdmin)
admin.site.register(Agency, AgencyAdmin)
admin.site.register(News, NewsAdmin)

# administration of publications - article proxy models
admin.site.register(ArticleBook, ArticleBookAdmin)
admin.site.register(ArticleArticle, ArticleArticleAdmin)
admin.site.register(ArticleConference, ArticleConferenceAdmin)
