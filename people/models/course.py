from django.core.validators import RegexValidator
from django.db import models

import multilingual
from people.models import Person


class Course(models.Model):
    lectors = models.ManyToManyField(Person)
    code = models.CharField(max_length=10, unique=True, validators=[RegexValidator(r'^[A-Z]{4}[0-9]{3}$')])
    LS = models.CharField(max_length=8, blank=True, null=True, validators=[RegexValidator(r'^[0-9]/[0-9] (Z|Zk|KZ|Z,Zk)$')])
    ZS = models.CharField(max_length=8, blank=True, null=True, validators=[RegexValidator(r'^[0-9]/[0-9] (Z|Zk|KZ|Z,Zk)$')])

    class Translation(multilingual.Translation):
        name = models.CharField(max_length=200)
        annotation = models.CharField(max_length=200, blank=True, null=True)
        note = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        app_label = 'people'


class Attachment(models.Model):
    course = models.ForeignKey(Course)
    title = models.CharField(max_length=200)
    file = models.FileField(max_length=200, upload_to='files/courses')

    class Meta:
        app_label = 'people'
        unique_together = (('course', 'title'),)

