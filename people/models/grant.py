from datetime import date

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

import multilingual
from people.models import Person


class Grant(models.Model):
    author = models.ForeignKey(Person)
    number = models.CharField(max_length=20)
    start = models.SmallIntegerField(validators=[MinValueValidator(1990), MaxValueValidator(date.today().year + 1)])
    end = models.SmallIntegerField(validators=[MinValueValidator(1990), MaxValueValidator(date.today().year + 10)])
    co_authors = models.ManyToManyField(Person, related_name='grant_related', blank=True, null=True)

    class Translation(multilingual.Translation):
        title = models.CharField(max_length=200)
        agency = models.CharField(max_length=200)
        annotation = models.TextField()

        class Meta:
            unique_together = (('number', 'agency'),)

    class Meta:
        app_label = 'people'

