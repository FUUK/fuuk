# coding: utf-8
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from multilingual import MultilingualModel

from fuuk.people.models import Place

nickname_validator = RegexValidator('^\w+$')

PERSON_TYPES = (
    ('STAFF', _('Academic staff')),
    ('OTHER', _('Other staff')),
    ('PHD', _('PhD. student')),
    ('MGR', _('Mgr. student')),
    ('BC', _('Bc. student')),
    ('GRAD', _('Graduate')),
    ('STUDENT', _('Student')),
)


class Human(MultilingualModel):
    """
    Collects persons for single human
    Used for history
    """
    user = models.OneToOneField(User, blank=True, null=True)
    nickname = models.CharField(
        max_length=20, unique=True,
        validators = [nickname_validator]
    )
    birth_date = models.DateField(blank=True, null=True)
    birth_place = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True, unique=True)
    photo = models.ImageField(max_length=200, blank=True, null=True, upload_to='img/person')
    display_posters = models.BooleanField(default=True, help_text=_('Uncheck to hide posters on your personal page.'))
    display_talks = models.BooleanField(default=True, help_text=_('Uncheck to hide talks not presented by you on your personal page.'))
    homepage = models.URLField(
        max_length=255,
        blank=True, null=True,
        help_text='Fill in form of www.link.com/subpage'
    )
    cv_file = models.FileField(max_length=200, blank=True, upload_to='cv')

    class Translation:
        subtitle = models.CharField(max_length=200, blank=True, null=True)
        cv = models.TextField(blank=True, null=True)
        interests = models.TextField(blank=True, null=True, help_text=_('Use Textile (http://en.wikipedia.org/wiki/Textile_(markup_language)) and &amp;#8209; for endash.'))
        stays = models.TextField(blank=True, null=True)

    class Meta:
        app_label = 'people'
        ordering = ('nickname',)

    def __unicode__(self):
        return self.nickname or u""


class Person(models.Model):
    # functional fields
    is_active = models.BooleanField(default=True)
    human = models.ForeignKey(Human, blank=True, null=True)
    type = models.CharField(max_length=10, blank=True, null=True, choices=PERSON_TYPES)
    advisor = models.ForeignKey('Person', related_name='student', blank=True, null=True)
    place = models.ManyToManyField(
        Place, blank=True, null=True,
        help_text=_('Only used for grant (co-)applicants or staff.')
    )
    # data fields
    prefix = models.CharField(max_length=20, blank=True, null=True)
    first_name = models.CharField(
        max_length=50,
        help_text=_('Only first letter is required for article authors. In case of multiple first names, fill them separated by space.')
    )
    last_name = models.CharField(max_length=50)
    suffix = models.CharField(max_length=20, blank=True, null=True)
    class_year = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        app_label = 'people'
        ordering = ('last_name',)
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

    @property
    def name(self):
        # e.g. for articles
        # should be used when titles are not displayed
        first_names = self.first_name.split(' ')
        first_names = ['%s.' % name[0] for name in first_names]
        return u"%s %s" % (
            self.last_name,
            ''.join(first_names)
        )

    @property
    def name_reversed(self):
        # for articles
        first_names = self.first_name.split(' ')
        first_names = ['%s.' % name[0] for name in first_names]
        return u"%s %s" % (
            ''.join(first_names), self.last_name
        )

    @property
    def full_name(self):
        return u"%s%s %s%s" % (
            self.prefix and u"%s " % self.prefix or u"",
            self.first_name,
            self.last_name,
            self.suffix and u", %s" % self.suffix or u"",
        )
