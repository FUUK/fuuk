from django.contrib import admin

from people.admin.options import PlaceAdmin, DepartmentAdmin, PersonAdmin, HumanAdmin, CourseAdmin, AttachmentAdmin, \
    GrantAdmin, ArticleAdmin, AuthorAdmin, ThesisAdmin, \
    ArticleBookAdmin, ArticleArticleAdmin, ArticleTalkAdmin, ArticlePosterAdmin
from people.models import Department, Place, Human, Person, Course, Attachment, Grant, Article, Author, Thesis, \
    ArticleBook, ArticleArticle, ArticleTalk, ArticlePoster


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

# administration of publications - article proxy models
admin.site.register(ArticleBook, ArticleBookAdmin)
admin.site.register(ArticleArticle, ArticleArticleAdmin)
admin.site.register(ArticleTalk, ArticleTalkAdmin)
admin.site.register(ArticlePoster, ArticlePosterAdmin)
