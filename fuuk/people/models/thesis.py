from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _
from multilingual import MultilingualModel

from fuuk.people.models import Person

THESIS_TYPES = (
    ('STUD', _('Student project')), 
    ('BC', _('Bachelor')),
    ('MGR', _('Master')),
    ('PHD', _('Doctoral')),
    ('RNDR', _('Rigorous')),
    ('PROF', _('Professor')),
)


class Thesis(MultilingualModel):
    type = models.CharField(max_length=5, choices=THESIS_TYPES)
    year = models.SmallIntegerField(validators=[MinValueValidator(1990)], help_text=_('Year of thesis start or year of defence if already defended.'))
    author = models.ForeignKey(Person)
    advisor = models.ForeignKey(Person, related_name='thesis_lead', blank=True, null=True)
    consultants = models.ManyToManyField(Person, related_name='thesis_consulted', blank=True, null=True)
    defended = models.BooleanField(default=False)
    thesis_file = models.FileField(max_length=200, blank=True, upload_to='thesis')

    class Translation:
        title = models.CharField(max_length=200)
        annotation = models.TextField(blank=True, null=True)
        abstract = models.TextField(blank=True, null=True)
        keywords = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        app_label = 'people'

    def __unicode__(self):
        return self.title or u""

    def clean(self):
        if self.advisor:
            # Check human if possible
            if self.author.human:
                if self.author.human == self.advisor.human:
                    raise ValidationError('Author can not be advisor.')
            else:
                if self.author == self.advisor:
                    raise ValidationError('Author can not be advisor.')

        # Many-to-many fields can only be checked if instance is already saved
        if self.pk and self.consultants.all():
            # Check human if possible
            if self.author.human:
                if self.author.human in self.consultants.values_list('human', flat=True):
                    raise ValidationError('Author can not be consultant.')
            else:
                if self.author in self.consultants.all():
                    raise ValidationError('Author can not be consultant.')

            # Check human if possible
            if self.advisor.human:
                if self.advisor.human in self.consultants.values_list('human', flat=True):
                    raise ValidationError('Advisor can not be consultant.')
            else:
                if self.advisor in self.consultants.all():
                    raise ValidationError('Advisor can not be consultant.')
