# coding: utf-8
from django.core.validators import RegexValidator
from django.db import models
from multilingual import MultilingualModel

phone_validator = RegexValidator(r'^\+420( [0-9]{3}){3}$')


class Department(MultilingualModel):
    fax = models.CharField(max_length=20, blank=True, null=True, unique=True, validators=[phone_validator])

    class Translation:
        name = models.CharField(max_length=200)

    class Meta:
        app_label = 'people'

    def __unicode__(self):
        if self.fax:
            return u'%s %s' % (self.name_any, self.fax)
        else:
            return self.name_any or u""


class Place(MultilingualModel):
    department = models.ForeignKey(Department, blank=True, null=True)
    phone = models.CharField(max_length=20, unique=True, validators=[phone_validator])

    class Translation:
        name = models.CharField(max_length=200)

    class Meta:
        app_label = 'people'

    def __unicode__(self):
        if self.department:
            return u'%s %s' % (self.name_any, self.department)
        else:
            return self.name_any or u""
