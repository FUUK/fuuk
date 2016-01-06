# coding: utf-8
from django.core.validators import RegexValidator
from django.db import models

phone_validator = RegexValidator(r'^\+420( [0-9]{3}){3}$')


class Department(models.Model):
    name = models.CharField(max_length=200)
    fax = models.CharField(max_length=20, blank=True, null=True, unique=True, validators=[phone_validator])

    class Meta:
        app_label = 'people'

    def __unicode__(self):
        if self.fax:
            return u'%s %s' % (self.name, self.fax)
        else:
            return self.name or u""


class Place(models.Model):
    department = models.ForeignKey(Department, blank=True, null=True)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, unique=True, blank=True, null=True, validators=[phone_validator])

    class Meta:
        app_label = 'people'

    def __unicode__(self):
        if self.department:
            return u'%s %s' % (self.name, self.department)
        else:
            return self.name or u""
