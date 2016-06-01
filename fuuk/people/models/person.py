# coding: utf-8
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from fuuk.common.forms import get_markdown_help_text
from fuuk.people.utils import sanitize_filename

from .place import Place

nickname_validator = RegexValidator(r'^\w+$')

PERSON_TYPES = (
    ('STAFF', _('Academic staff')),
    ('OTHER', _('Other staff')),
    ('PHD', _('PhD. student')),
    ('MGR', _('Mgr. student')),
    ('BC', _('Bc. student')),
    ('GRAD', _('Graduate student')),
    ('STUDENT', _('Student')),
)


def image_filename(instance, filename):
    return sanitize_filename(filename, 'img/person')


def cv_filename(instance, filename):
    return sanitize_filename(filename, 'cv')


class Human(models.Model):
    """
    Collects persons for single human
    Used for history
    """
    user = models.OneToOneField(User, blank=True, null=True)
    nickname = models.CharField(
        max_length=20, unique=True,
        validators=[nickname_validator]
    )
    birth_date = models.DateField(blank=True, null=True)
    birth_place = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True, unique=True)
    photo = models.ImageField(max_length=200, blank=True, null=True, upload_to=image_filename)
    display_posters = models.BooleanField(default=True, help_text=_('Uncheck to hide posters on your personal page.'))
    display_talks = models.BooleanField(
        default=True,
        help_text=_('Uncheck to hide talks not presented by you on your personal page.')
    )
    homepage = models.URLField(
        max_length=255,
        blank=True, null=True,
        help_text='Fill in form of www.link.com/subpage'
    )
    cv_file = models.FileField(max_length=200, blank=True, upload_to=cv_filename)
    subtitle = models.CharField(max_length=200, blank=True, null=True)
    cv = models.TextField(blank=True, null=True, help_text=get_markdown_help_text)
    interests = models.TextField(blank=True, null=True, help_text=get_markdown_help_text)
    stays = models.TextField(blank=True, null=True, help_text=get_markdown_help_text)

    class Meta:
        app_label = 'people'

    def __unicode__(self):
        return self.nickname or u""


class Person(models.Model):
    # functional fields
    is_active = models.BooleanField(default=True)
    human = models.ForeignKey(Human, blank=True, null=True)
    type = models.CharField(max_length=10, blank=True, null=True, choices=PERSON_TYPES)
    advisor = models.ForeignKey('Person', related_name='student', blank=True, null=True)
    place = models.ManyToManyField(
        Place, blank=True,
        help_text=_('Only used for grant (co-)applicants or staff.')
    )
    # data fields
    prefix = models.CharField(max_length=20, blank=True, null=True)
    first_name = models.CharField(
        max_length=50,
        help_text=_('Only first letter is required for article authors. In case of multiple first names, fill them '
                    'separated by space.')
    )
    last_name = models.CharField(max_length=50)
    suffix = models.CharField(max_length=20, blank=True, null=True)
    class_year = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        app_label = 'people'
        unique_together = (
            ('first_name', 'last_name', 'type'),
        )

    def __unicode__(self):
        if self.type:
            return u"%s %s (%s)" % (self.last_name, self.first_name, self.get_type_display())
        else:
            return u"%s %s" % (self.last_name, self.first_name)

    def clean(self):
        if self.human:
            if self.is_active and Person.objects.exclude(pk=self.pk).filter(human=self.human, is_active=True):
                raise ValidationError(_('Only one person can be active per human.'))
        else:
            if self.type:
                raise ValidationError(_('Person with type must have human.'))

        if self.type in ('PHD', 'MGR', 'BC') and not self.class_year:
            raise ValidationError(_('Students must have class year.'))

        if self.advisor and not self.human:
            raise ValidationError(_('Students with assigned advisor must have "human".'))

    @property
    def name(self):
        # e.g. for articles
        # should be used when titles are not displayed
        first_names = self.first_name.split()
        first_names = ['%s.' % name[0] for name in first_names]
        return u"%s %s" % (
            self.last_name.strip(),
            ''.join(first_names)
        )

    @property
    def name_reversed(self):
        # for articles
        first_names = self.first_name.split()
        first_names = ['%s.' % name[0] for name in first_names]
        return u"%s %s" % (
            ''.join(first_names), self.last_name.strip()
        )

    @property
    def full_name(self):
        if self.prefix:
            prefix = self.prefix.strip()
        else:
            prefix = ''
        if self.suffix:
            suffix = self.suffix.strip()
        else:
            suffix = ''
        first_names = self.first_name.split()
        first_names = ['%s ' % name for name in first_names]
        return u"%s%s%s%s" % (
            prefix and u"%s " % prefix or u"",
            ''.join(first_names),
            self.last_name.strip(),
            suffix and u", %s" % suffix or u"",
        )
