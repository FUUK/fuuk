from django.contrib.flatpages.forms import FlatpageForm as _FlatpageForm

from .models import FlatPage


class FlatpageForm(_FlatpageForm):
    """
    Flatpage form based on our FlatPage model.
    """
    class Meta(_FlatpageForm.Meta):
        model = FlatPage
