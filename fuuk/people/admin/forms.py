from django import forms
from django.utils.translation import ugettext_lazy as _

from fuuk.people.admin.fields import NullCharField
from fuuk.people.models import ARTICLE_TYPES


class ArticleBookForm(forms.ModelForm):
    type = forms.ChoiceField(initial = 'BOOK', choices = (('BOOK', _('Book')),))
    identification = NullCharField(label=_('ISBN'), max_length=100, required=False)
    publication = NullCharField(label=_('Book title'), max_length=100)
    page_to = NullCharField(max_length=10, required=False, help_text=_('Leave blank for one-paged chapters.'))

    class Meta:
        fields = (
            'type', 'accepted', 'identification', 'year', 'title', 'publication', 'page_from', 'page_to',
            'editors', 'publishers', 'place'
        )


class ArticleArticleForm(forms.ModelForm):
    type = forms.ChoiceField(initial = 'ARTICLE', choices = (('ARTICLE', _('Article')),))
    identification = NullCharField(max_length=100, required=False, label=_('DOI'),
                                   help_text=_('Without leading http://dx.doi.org/'))
    publication = NullCharField(max_length=100, label=_('Journal'), help_text=_('Full name of journal'))
    page_to = NullCharField(max_length=10, required=False, help_text=_('Leave blank for one-paged articles.'))

    class Meta:
        fields = (
            'type', 'accepted', 'identification', 'year', 'title', 'publication',
            'volume', 'issue', 'page_from', 'page_to'
        )


#TODO: narrow select for 'presenter' only to authors already added
conference_choices = [(key, value) for key, value in ARTICLE_TYPES if key in ('TALK', 'INVITED', 'POSTER')]

class ArticleConferenceForm(forms.ModelForm):
    type = forms.ChoiceField(choices = conference_choices)
    publication = NullCharField(label=_('Abstract collection'), max_length=100, required=False)
    place = NullCharField(max_length=200, required=False, help_text=_('City, state, date.'))

    class Meta:
        fields = ('type', 'year', 'title', 'presenter', # talk data
                  'publication', 'volume', 'page_from', 'page_to', 'editors', 'place' # abstract collection data
        )
