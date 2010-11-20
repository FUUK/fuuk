from django.core.exceptions import ValidationError
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
    identification = models.CharField(max_length=25, blank=True, null=True, unique=True)
    year = models.SmallIntegerField(validators=[MinValueValidator(1990)])
    title = models.CharField(max_length=200)

    ### PUBLICATION INFO
    # journal for ARTICLE, PROCEEDING (required)
    # book title for BOOK (required)
    # abstract collection for TALK, POSTER (not required)
    publication = models.CharField(max_length=50, blank=True, null=True)
    # only ARTICLE
    volume = models.CharField(max_length=10, blank=True, null=True) #TODO: integer?
    # required for BOOK, ARTICLE, PROCEEDING
    page_from = models.SmallIntegerField(blank=True, null=True)
    page_to = models.SmallIntegerField(blank=True, null=True)
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

    def clean(self):
        if self.type == 'BOOK':
            if not self.identification:
                raise ValidationError(_('Book has to have ISBN number.'))
            if not self.publication:
                raise ValidationError(_('Book has to have book title.'))
            if self.volume:
                raise ValidationError(_('Book can not have volume.'))
            if not self.page_from or not self.page_to:
                raise ValidationError(_('Book has to have pages.'))
            if not self.editors:
                raise ValidationError(_('Book has to have publishers.'))
            if self.length:
                raise ValidationError(_('Book can not have length.'))
            if self.presenter:
                raise ValidationError(_('Book can not have presenter.'))
        elif self.type == 'ARTICLE':
            if not self.identification:
                raise ValidationError(_('Article has to have DOI number.'))
            if not self.publication:
                raise ValidationError(_('Article has to have journal.'))
            if not self.volume:
                raise ValidationError(_('Article has to have volume.'))
            if not self.page_from or not self.page_to:
                raise ValidationError(_('Article has to have pages.'))
            if self.editors:
                raise ValidationError(_('Article can not have editors.'))
            if self.place:
                raise ValidationError(_('Article can not have place.'))
            if self.length:
                raise ValidationError(_('Article can not have length.'))
            if self.presenter:
                raise ValidationError(_('Article can not have presenter.'))
        elif self.type == 'PROCEEDING':
            if not self.identification:
                raise ValidationError(_('Proceeding has to have ISBN number.'))
            if not self.publication:
                raise ValidationError(_('Proceeding has to have journal.'))
            if self.volume:
                raise ValidationError(_('Proceeding can not have volume.'))
            if not self.page_from or not self.page_to:
                raise ValidationError(_('Proceeding has to have pages.'))
            if not self.editors:
                raise ValidationError(_('Proceeding has to have editors.'))
            if self.length:
                raise ValidationError(_('Proceeding can not have length.'))
            if self.presenter:
                raise ValidationError(_('Proceeding can not have presenter.'))
        elif self.type == 'TALK':
            if self.identification:
                raise ValidationError(_('Talk can not have ISBN/DOI number.'))
            if self.volume:
                raise ValidationError(_('Talk can not have volume.'))
            if self.page_from or self.page_to:
                raise ValidationError(_('Talk can not have pages.'))
        elif self.type == 'POSTER':
            if self.identification:
                raise ValidationError(_('Poster can not have ISBN/DOI number.'))
            if self.volume:
                raise ValidationError(_('Poster can not have volume.'))
            if self.page_from or self.page_to:
                raise ValidationError(_('Poster can not have pages.'))
            if self.length:
                raise ValidationError(_('Poster can not have length.'))
        if self.presenter and self.presenter not in self.author_set.all():
            raise ValidationError(_('Presenter must be among authors.'))

    @property
    def citation(self):
        #TODO: would be inclusion tag better, when html tags will be used?
        authors = [author.person.name for author in self.author_set.select_related('person').order_by('order')]
        details = []
        if self.publication:
            details.append(" %s" % self.publication)
        if self.volume:
            details.append(" %s" % self.volume)
        details.append("%s" % self.year)
        if self.page_from and self.page_to:
            details.append("%s-%s" % (self.page_from, self.page_to))

        return u"%s: %s. %s" % (
            ', '.join(authors),
            self.title,
            ', '.join(details)
        )


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

    def clean(self):
        if self.order > 1 \
        and self.article.author_set.exclude(pk=self.pk).filter(order__lt=self.order).count() != (self.order - 1):
            raise ValidationError('Authors must be added in order.')
