from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class FlatPagesConfig(AppConfig):
    name = 'fuuk.fuflatpages'
    verbose_name = _("Flat Pages")
