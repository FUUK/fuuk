from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, RegexValidator, URLValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .person import Person

ARTICLE_TYPES = (
    ('BOOK', _('Book')),
    ('ARTICLE', _('Article')),
    ('TALK', _('Lecture')),
    ('INVITED', _('Invited lecture')),  # almost same as TALK
    ('POSTER', _('Poster')),
)

doi_validator = RegexValidator(r'^10\.[0-9]{4}.*$')
# 978 (code for book publishing), group id, publisher code, title code, checksum, separated by dash or space
# see ISBN at wikipedia for more info :)
isbn_validator = RegexValidator(r'^(978[- ])?[0-9]{1,5}[- ][0-9]{1,6}[- ][0-9]{1,7}[- ][0-9]$')
page_validator = RegexValidator(r'^[A-Z]{0,2}[0-9]+(-[0-9]+)?$')  # numbers or form 'AA1857'
volume_issue_validator = RegexValidator(r'^[A-Z]?[0-9]{1,4}([-/][0-9]{1,4})?$')  # numbers with slashes or dashes


class Article(models.Model):
    # COMMON INFO
    type = models.CharField(max_length=10, choices=ARTICLE_TYPES)
    # DOI for ARTICLE (not required); ISBN for BOOK (required)
    identification = models.CharField(max_length=100, blank=True, null=True, unique=True)
    year = models.SmallIntegerField(validators=[MinValueValidator(1979)])
    title = models.CharField(max_length=300)
    accepted = models.BooleanField(
        help_text=_('Mark this article as accepted only. No volume and pages has to be filled in.'),
        default=False
    )

    # PUBLICATION INFO
    # journal for ARTICLE (required)
    # book title for BOOK (required)
    # abstract collection for TALK, POSTER (not required)
    publication = models.CharField(max_length=100, blank=True, null=True)

    # only ARTICLE
    volume = models.CharField(validators=[volume_issue_validator], max_length=10, blank=True, null=True)
    issue = models.CharField(validators=[volume_issue_validator], max_length=10, blank=True, null=True)

    # required for BOOK, ARTICLE
    page_from = models.CharField(max_length=10, blank=True, null=True, validators=[page_validator])
    article_number = models.BooleanField(help_text=_('Check if the journal is using article numbers instead of pages'),
                                         default=False)
    page_to = models.CharField(max_length=10, blank=True, null=True, validators=[page_validator],
                               help_text=_('Leave blank for one paged abstracts.'))

    # optional for TALK, POSTER, BOOK
    editors = models.CharField(max_length=200, blank=True, null=True)

    # required for BOOK
    publishers = models.CharField(max_length=200, blank=True, null=True)

    # only BOOK, TALK, POSTER
    place = models.CharField(max_length=200, blank=True, null=True)

    # only TALK, POSTER
    presenter = models.ForeignKey(
        Person, blank=True, null=True,
        help_text=_('Before selecting a presenter fill authors and press "Save and continue editing".')
    )

    class Meta:
        app_label = 'people'
        unique_together = (
            ('year', 'publication', 'volume', 'page_from', 'page_to'),
        )

    def __unicode__(self):
        return self.title or u""

    def clean(self):
        if self.type == 'BOOK':
            if self.presenter:
                raise ValidationError(_('Book can not have presenter.'))
            if self.volume:
                raise ValidationError(_('Book can not have volume.'))

            if self.accepted:
                return

            if self.identification:
                try:
                    isbn_validator(self.identification)
                except ValidationError:
                    raise ValidationError('Enter valid ISBN.')
            else:
                raise ValidationError(_('Book has to have ISBN number.'))

            if not self.publication:
                raise ValidationError(_('Book has to have book title.'))
            if not self.page_from:
                raise ValidationError(_('Book has to have page(s).'))
            if not self.publishers:
                raise ValidationError(_('Book has to have publishers.'))
        elif self.type == 'ARTICLE':
            if self.editors:
                raise ValidationError(_('Article can not have editors.'))
            if self.publishers:
                raise ValidationError(_('Article can not have publishers.'))
            if self.place:
                raise ValidationError(_('Article can not have place.'))
            if self.presenter:
                raise ValidationError(_('Article can not have presenter.'))

            if self.accepted:
                return

            if self.identification:
                try:
                    doi_validator(self.identification)
                    URLValidator('http://dx.doi.org/%s' % self.identification)
                except ValidationError:
                    raise ValidationError('Enter valid DOI.')

            if not self.publication:
                raise ValidationError(_('Article has to have journal.'))
            if not self.volume:
                raise ValidationError(_('Article has to have volume.'))
            if not self.page_from:
                raise ValidationError(_('Article has to have page(s).'))
            elif not self.article_number and self.page_to and (self.page_to < self.page_from):
                raise ValidationError(_('End page number must be bigger than start page number.'))
        elif self.type in ('TALK', 'INVITED', 'POSTER'):
            if self.accepted:
                raise ValidationError(_('Conference paper can not be accepted.'))
            if self.identification:
                raise ValidationError(_('Conference paper can not have ISBN/DOI number.'))
            if self.volume:
                raise ValidationError(_('Conference paper can not have volume.'))
            if self.publishers:
                raise ValidationError(_('Conference paper can not have publishers.'))
            if not self.page_from and self.page_to:
                raise ValidationError(_('Page from must be filled if pages are specified.'))
            elif self.page_to and (self.page_to < self.page_from):
                raise ValidationError(_('End page number must be bigger than start page number.'))
        if self.presenter and not self.author_set.filter(person=self.presenter):
            raise ValidationError(_('Presenter must be one of authors.'))


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


###############################################################################
# Article proxy models

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
