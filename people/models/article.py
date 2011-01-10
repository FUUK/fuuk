from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

import multilingual
from people.models import Person

ARTICLE_TYPES = (
    ('BOOK', _('Book')),
    ('ARTICLE', _('Article')),
    ('TALK', _('Lecture')),
    ('INVITED', _('Invited lecture')), # almost same as TALK
    ('POSTER', _('Poster')),
)

page_validator = RegexValidator(r'^[A-Z]?[0-9]+$') # numbers or form 'A1857'


class Article(models.Model):

    ### ARTICLE INFO
    type = models.CharField(max_length=10, choices=ARTICLE_TYPES)
    # DOI for ARTICLE (not required); ISBN for BOOK (required)
    identification = models.CharField(max_length=100, blank=True, null=True, unique=True)
    year = models.SmallIntegerField(validators=[MinValueValidator(1990)])
    title = models.CharField(max_length=300)

    ### PUBLICATION INFO
    # journal for ARTICLE (required)
    # book title for BOOK (required)
    # abstract collection for TALK, POSTER (not required)
    publication = models.CharField(max_length=100, blank=True, null=True)
    # only ARTICLE
    volume = models.CharField(max_length=10, blank=True, null=True) #TODO: integer?
    # required for BOOK, ARTICLE
    page_from = models.CharField(max_length=10, blank=True, null=True, validators=[page_validator])
    page_to = models.CharField(max_length=10, blank=True, null=True, validators=[page_validator])
    # editors for TALK, POSTER (not required)
    # publishers for BOOK (required)
    editors = models.CharField(max_length=200, blank=True, null=True)
    # only BOOK, TALK, POSTER
    place = models.CharField(max_length=200, blank=True, null=True)

    ### PRESENTATION INFO
    # only TALK, POSTER
    presenter = models.ForeignKey(Person, blank=True, null=True)

    class Meta:
        app_label = 'people'
        unique_together = (
            ('year', 'publication', 'volume', 'page_from', 'page_to'),
        )

    def __unicode__(self):
        return self.title or u""

    def clean(self):
        if self.type == 'BOOK':
            if not self.identification:
                raise ValidationError(_('Book has to have ISBN number.'))
            if not self.publication:
                raise ValidationError(_('Book has to have book title.'))
            if self.volume:
                raise ValidationError(_('Book can not have volume.'))
            if not self.page_from:
                raise ValidationError(_('Book has to have page(s).'))
            if not self.editors:
                raise ValidationError(_('Book has to have publishers.'))
            if self.presenter:
                raise ValidationError(_('Book can not have presenter.'))
        elif self.type == 'ARTICLE':
            if not self.publication:
                raise ValidationError(_('Article has to have journal.'))
            if not self.volume:
                raise ValidationError(_('Article has to have volume.'))
            if not self.page_from:
                raise ValidationError(_('Article has to have page(s).'))
            if self.editors:
                raise ValidationError(_('Article can not have editors.'))
            if self.place:
                raise ValidationError(_('Article can not have place.'))
            if self.presenter:
                raise ValidationError(_('Article can not have presenter.'))
        elif self.type in ('TALK', 'INVITED', 'POSTER'):
            if self.identification:
                raise ValidationError(_('Talk can not have ISBN/DOI number.'))
            if self.volume:
                raise ValidationError(_('Talk can not have volume.'))
            if not self.page_from and self.page_to:
                raise ValidationError(_('Page from must be filled if pages are specified.'))
        if self.presenter and not self.author_set.filter(person=self.presenter):
            raise ValidationError(_('Presenter must be among authors.'))


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
        return u'%s %s (%s)' % (self.person, self.article, self.order)

    def save(self, *args, **kwargs):
        if self.order is None:
            self.order = Author.objects.filter(article=self.article).count() + 1
        return super(Author, self).save(*args, **kwargs)


### Article proxy models

class ArticleBook(Article):
    class Meta:
        app_label = 'publications'
        proxy = True
        verbose_name = _('Book')
        verbose_name_plural = _('Books')


class ArticleArticle(Article):
    class Meta:
        app_label = 'publications'
        proxy = True
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')


class ArticleConference(Article):
    class Meta:
        app_label = 'publications'
        proxy = True
        verbose_name = _('Conference paper')
        verbose_name_plural = _('Conference paper')
