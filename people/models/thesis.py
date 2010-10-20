from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

import multilingual
from people.models import Person

THESIS_TYPES = (
    ('BC', _('Bachelor')),
    ('MGR', _('Master')),
    ('PHD', _('Doctoral')),
    ('RNDR', _('Rigorous')),
    ('PROF', _('Professor')),
)

class Thesis(models.Model):
    type = models.CharField(max_length=5, choices=THESIS_TYPES)
    year = models.SmallIntegerField(validators=[MinValueValidator(1990)])
    author = models.ForeignKey(Person)
    advisor = models.ForeignKey(Person, related_name='thesis_lead', blank=True, null=True)
    consultants = models.ManyToManyField(Person, related_name='thesis_consulted', blank=True, null=True)

    class Translation(multilingual.Translation):
        title = models.CharField(max_length=200)
        annotation = models.TextField(blank=True, null=True)
        abstract = models.TextField(blank=True, null=True)
        keywords = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        app_label = 'people'

