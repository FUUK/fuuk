from django.db import models
from django.utils.translation import ugettext_lazy as _

from .place import Institution


class AbstractAuthor(models.Model):
    '''
    Abstract base class for author
    '''
    first_name = models.CharField(_('first name'), max_length=50)
    last_name = models.CharField(_('last name'), max_length=50)

    class Meta:
        abstract = True


class AbstractFullAuthor(AbstractAuthor):
    '''
    abstract base class for authors with prefix and suffix
    '''
    prefix = models.CharField(_('prefix'), max_length=20, blank=True, null=True)
    suffix = models.CharField(_('suffix'), max_length=20, blank=True, null=True)
    institution = models.ForeignKey(Institution, blank=True, null=True, on_delete=models.SET_NULL,
                                    verbose_name=_('institution'))

    class Meta(AbstractAuthor.Meta):
        abstract = True
