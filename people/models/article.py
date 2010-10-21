# coding: utf-8
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

import multilingual
from people.models import Person

ARTICLE_TYPES = (
    ('BOOK', _('Book')),
    ('ARTICLE', _('Article')),
    ('PROCEEDING', _('Proceeding')),
    ('TALK', _('Talk')),
    ('POSTER', _('Poster')),
)


# TODO: proxy models?
class Article(models.Model):

    ### ARTICLE INFO
    type = models.CharField(max_length=10, choices=ARTICLE_TYPES)
    # DOI for ARTICLE (required)
    # ISBN for BOOK, PROCEEDING (required)
    identification = models.CharField(max_length=15, blank=True, null=True, unique=True)
    year = models.SmallIntegerField(validators=[MinValueValidator(1990)])
    title = models.CharField(max_length=200)

    ### PUBLICATION INFO
    # journal for ARTICLE, PROCEEDING (required)
    # book title for BOOK (required)
    # abstract collection for TALK, POSTER (not required)
    publication = models.CharField(max_length=50, blank=True, null=True)
    # only PAPER
    volume = models.CharField(max_length=10, blank=True, null=True) #TODO: integer?
    page_from = models.SmallIntegerField(blank=True, null=True) # required for BOOK, ARTICLE, PROCEEDING
    page_to = models.SmallIntegerField(blank=True, null=True) # required for BOOK, ARTICLE, PROCEEDING
    # editors for PROCEEDING (required), TALK, POSTER (not required)
    # publishers for BOOK (required)
    editors = models.CharField(max_length=200, blank=True, null=True)
    # only BOOK, PROCEEDING, TALK, POSTER
    place = models.CharField(max_length=200, blank=True, null=True)

    ### PRESENTATION INFO
    # only TALK, in minutes
    length = models.SmallIntegerField(blank=True, null=True)
    # only TALK, POSTER
    presenter = models.ForeignKey(Person, blank=True, null=True)

    class Meta:
        app_label = 'people'
        unique_together = (
            ('year', 'publication', 'volume', 'page_from', 'page_to'),
        )

    def __unicode__(self):
        return self.title

class Author(models.Model):
    person = models.ForeignKey(Person)
    article = models.ForeignKey(Article)
    order = models.SmallIntegerField()

    class Meta:
        app_label = 'people'
        unique_together = (
            ('person', 'article'),
            ('article', 'order'),
        )

    def __unicode__(self):
        return self.person.human.nickname

