from django.core.validators import RegexValidator
from django.db import models
from multilingual import MultilingualModel

from fuuk.people.models import Person


code_validator = RegexValidator(r'^[A-Z]{2}([A-Z]{2}[0-9]{3}|[0-9]{3}[A-Z][0-9]{2}[A-Z]?)$') # MFF | PrF
hours_validator = RegexValidator(r'^[0-9]/[0-9] (Z|Zk|KZ|Zk/Z)$')


class Course(MultilingualModel):
    lectors = models.ManyToManyField(Person)
    practical_lectors = models.ManyToManyField(Person, blank=True, null=True, related_name='practical_course_set')
    code = models.CharField(max_length=10, unique=True, validators=[code_validator])
    ls = models.CharField(max_length=8, blank=True, null=True, validators=[hours_validator])
    zs = models.CharField(max_length=8, blank=True, null=True, validators=[hours_validator])

    class Translation:
        name = models.CharField(max_length=200)
        annotation = models.TextField(blank=True, null=True)
        note = models.TextField(blank=True, null=True)

    class Meta:
        app_label = 'people'

    def __unicode__(self):
        return self.name or u""


class Attachment(models.Model):
    course = models.ForeignKey(Course)
    title = models.CharField(max_length=200)
    file = models.FileField(max_length=200, upload_to='files/courses')

    class Meta:
        app_label = 'people'
        unique_together = (('course', 'title'),)

    def __unicode__(self):
        return self.title or u""
