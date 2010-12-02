# coding: utf-8
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

import multilingual
from people.models import Place

PERSON_TYPES = (
    ('STAFF', _('Staff')),
    ('PHD', _('PhD. student')),
    ('MGR', _('Mgr. student')),
    ('BC', _('Bc. student')),
)


class Human(models.Model):
    """
    Collects persons for single human
    Used for history
    """
    nickname = models.CharField(max_length=20, unique=True) # just for overview
    birth_date = models.DateField(blank=True, null=True)
    birth_place = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True, unique=True)
    photo = models.ImageField(max_length=200, blank=True, null=True, upload_to='img/person')

    class Translation(multilingual.Translation):
        subtitle = models.CharField(max_length=200, blank=True, null=True)
        #TODO: these might require some markdown
        cv = models.TextField(blank=True, null=True)
        interests = models.TextField(blank=True, null=True)
        stays = models.TextField(blank=True, null=True)

    class Meta:
        app_label = 'people'

    def __unicode__(self):
        return self.nickname


class Person(models.Model):
    # functional fields
    is_active = models.BooleanField(default=True)
    human = models.ForeignKey(Human, blank=True, null=True) #required if type != None
    type = models.CharField(max_length=10, blank=True, null=True, choices=PERSON_TYPES)
    advisor = models.ForeignKey('Person', related_name='student', blank=True, null=True)
    place = models.ForeignKey(Place, blank=True, null=True)
    # data fields
    prefix = models.CharField(max_length=20, blank=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    suffix = models.CharField(max_length=20, blank=True, null=True)
    class_year = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        app_label = 'people'
        unique_together = (
            ('first_name', 'last_name', 'type'),
        )

    def __unicode__(self):
        return u"%s %s (%s)" % (self.first_name, self.last_name, self.human or '')

    def clean(self):
        #TODO: only one person per human can be active
        if self.type and not self.human:
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
    def full_name(self):
        return u"%s%s%s %s%s%s" % (
            self.prefix,
            self.prefix and ' ' or '',
            self.first_name,
            self.last_name,
            self.suffix and ', ' or '',
            self.suffix
        )
