from datetime import date

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from fuuk.common.forms import get_markdown_help_text

from ..utils import full_name
from .author import AbstractFullAuthor
from .person import Human
from .place import Institution


class Agency(models.Model):
    shortcut = models.CharField(max_length=10)
    name = models.CharField(max_length=100)

    class Meta:
        app_label = 'people'

    def __unicode__(self):
        return self.shortcut or u""


class Grant(models.Model):
    editor = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, verbose_name=_('editor'))
    investigator_prefix = models.CharField(_('prefix'), max_length=20, blank=True, null=True)
    investigator_first_name = models.CharField(_('first name'), max_length=50)
    investigator_last_name = models.CharField(_('last name'), max_length=50)
    investigator_suffix = models.CharField(_('suffix'), max_length=20, blank=True, null=True)
    investigator_institution = models.ForeignKey(Institution, blank=True, null=True, on_delete=models.CASCADE,
                                                 verbose_name=_('institution'))
    investigator_human = models.ForeignKey(Human, blank=True, null=True, on_delete=models.SET_NULL,
                                           verbose_name=_('human'))
    number = models.CharField(_('grant number'), max_length=20)
    start = models.SmallIntegerField(_('start year'), validators=[MinValueValidator(1990),
                                     MaxValueValidator(date.today().year + 1)])
    end = models.SmallIntegerField(_('end year'), validators=[MinValueValidator(1990),
                                   MaxValueValidator(date.today().year + 10)])
    agency = models.ForeignKey(Agency, help_text=_('Contact administrators for different Grant Agency.'),
                               verbose_name=_('grant agency'))

    title = models.CharField(_('title'), max_length=200)
    annotation = models.TextField(_('grant annotation'), help_text=get_markdown_help_text)

    class Meta:
        app_label = 'people'
        unique_together = (('number', 'agency'),)
        verbose_name = _('grant')
        verbose_name_plural = _('grants')

    def __unicode__(self):
        return self.title or u""

    @property
    def investigator_name(self):
        return u"%s %s" % (self.investigator_last_name, self.investigator_first_name)
    investigator_name.fget.short_description = _('applicant name')

    @property
    def investigator_full_name(self):
        return full_name(self.investigator_prefix, self.investigator_first_name, self.investigator_last_name,
                         self.investigator_suffix)
    investigator_full_name.fget.short_description = _('applicant full name')


class GrantCollaborator(AbstractFullAuthor):
    grant = models.ForeignKey(Grant, related_name='collaborators', on_delete=models.CASCADE, verbose_name=_('grant'))
    human = models.ForeignKey(Human, blank=True, null=True, on_delete=models.SET_NULL, verbose_name=_('human'))

    class Meta(AbstractFullAuthor.Meta):
        unique_together = (('human', 'grant'),)
        verbose_name = _('co-applicant')
        verbose_name_plural = _('co-applicants')

    def __unicode__(self):
        if self.human:
            return u"%s %s (%s)" % (self.last_name, self.first_name, self.human.nickname)
        else:
            return u"%s %s" % (self.last_name, self.first_name)

    @property
    def full_name(self):
        return full_name(self.prefix, self.first_name, self.last_name, self.suffix)
