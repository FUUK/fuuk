from django.contrib import admin

from fuuk.people.admin.options import (AgencyAdmin, ArticleArticleAdmin, ArticleBookAdmin, ArticleConferenceAdmin,
                                       AttachmentAdmin, CourseAdmin, DepartmentAdmin, GrantAdmin, HumanAdmin, NewsAdmin,
                                       InstitutionAdmin, PersonAdmin, PlaceAdmin, ThesisAdmin)
from fuuk.people.models import (Agency, ArticleArticle, ArticleBook, ArticleConference, Attachment, Course, Department,
                                Grant, Human, Institution, News, Person, Place, Thesis)

admin.site.register(Place, PlaceAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Human, HumanAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Attachment, AttachmentAdmin)
admin.site.register(Grant, GrantAdmin)
admin.site.register(Institution, InstitutionAdmin)
admin.site.register(Thesis, ThesisAdmin)
admin.site.register(Agency, AgencyAdmin)
admin.site.register(News, NewsAdmin)

# administration of publications - article proxy models
admin.site.register(ArticleBook, ArticleBookAdmin)
admin.site.register(ArticleArticle, ArticleArticleAdmin)
admin.site.register(ArticleConference, ArticleConferenceAdmin)
