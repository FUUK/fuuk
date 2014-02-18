from datetime import date

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from multilingual import MultilingualModel

from fuuk.people.models import Person


class Agency(MultilingualModel):
    class Translation:
        shortcut = models.CharField(max_length=10)
        name = models.CharField(max_length=100)

    class Meta:
        app_label = 'people'

    def __unicode__(self):
        return self.shortcut or u""


class Grant(MultilingualModel):
    author = models.ForeignKey(Person, verbose_name=_('Applicant'))
    number = models.CharField(max_length=20)
    start = models.SmallIntegerField(validators=[MinValueValidator(1990), MaxValueValidator(date.today().year + 1)])
    end = models.SmallIntegerField(validators=[MinValueValidator(1990), MaxValueValidator(date.today().year + 10)])
    co_authors = models.ManyToManyField(Person, related_name='grant_related', blank=True, null=True, verbose_name=_('Co-applicant'))
    agency = models.ForeignKey(Agency, help_text=_('Contact administrators for different Grant Agency.'))

    class Translation:
        title = models.CharField(max_length=200)
        annotation = models.TextField()

    class Meta:
        app_label = 'people'
        unique_together = (('number', 'agency'),)

    def __unicode__(self):
        return self.title or u""

    def clean(self):
        # Many-to-many fields can only be checked if instance is already saved
        if self.pk and self.co_authors.all():
            # Check human if possible
            if self.author.human:
                if self.author.human in self.co_authors.values_list('human', flat=True):
                    raise ValidationError('Author can not be also co_author.')
            else:
                if self.author in self.co_authors.all():
                    raise ValidationError('Author can not be also co_author.')
