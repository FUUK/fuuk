# coding: utf-8
from django.db import models
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

    class Meta:
        app_label = 'people'

    def __unicode__(self):
        return self.nickname


class Person(models.Model):
    # functional fields
    #is_active = models.BooleanField()
    human = models.ForeignKey(Human, blank=True, null=True) #required if type != None
    type = models.CharField(max_length=10, blank=True, null=True, choices=PERSON_TYPES)
    advisor = models.ForeignKey('Person', related_name='student', blank=True, null=True)
    place = models.ForeignKey(Place, blank=True, null=True)
    # data fields
    prefix = models.CharField(max_length=20, blank=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    suffix = models.CharField(max_length=20, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    birth_place = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True, unique=True)
    photo = models.ImageField(max_length=200, blank=True, null=True, upload_to='img/person')
    year = models.SmallIntegerField(blank=True, null=True)

    class Translation(multilingual.Translation):
        subtitle = models.CharField(max_length=200, blank=True, null=True)
        #TODO: these might require some markdown
        cv = models.TextField(blank=True, null=True)
        interests = models.TextField(blank=True, null=True)
        stays = models.TextField(blank=True, null=True)

    class Meta:
        app_label = 'people'
        unique_together = (
            ('first_name', 'last_name', 'type'),
        )

    def __unicode__(self):
        return '%s %s (%s)' % (self.first_name, self.last_name, self.human or '')
