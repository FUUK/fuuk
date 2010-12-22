from django import forms
from django.utils.translation import ugettext_lazy as _


class ArticleBookForm(forms.ModelForm):
    type = forms.ChoiceField(initial = 'BOOK', choices = (('BOOK', _('Book')),))
    identification = forms.CharField(label=_('ISBN'), max_length=25)
    publication = forms.CharField(label=_('Book title'), max_length=50)
    page_from = forms.CharField(max_length=10)
    page_to = forms.CharField(max_length=10, required=False)
    editors = forms.CharField(label=_('Publishers'), max_length=200)

    class Meta:
        fields = ('type', 'identification', 'year', 'title', 'publication', 'page_from', 'page_to', 'editors', 'place')


class ArticleArticleForm(forms.ModelForm):
    type = forms.ChoiceField(initial = 'ARTICLE', choices = (('ARTICLE', _('Article')),))
    identification = forms.CharField(label=_('DOI'), max_length=25)
    publication = forms.CharField(label=_('Journal'), max_length=50)
    volume = forms.CharField(max_length=10)
    page_from = forms.CharField(max_length=10)
    page_to = forms.CharField(max_length=10, required=False)

    class Meta:
        fields = ('type', 'identification', 'year', 'title', 'publication', 'volume', 'page_from', 'page_to')


#TODO: narrow select for 'presenter' only to authors already added

class ArticleTalkForm(forms.ModelForm):
    type = forms.ChoiceField(initial = 'TALK', choices = (('TALK', _('Talk')),))
    publication = forms.CharField(label=_('Abstract collection'), max_length=50, required=False)

    class Meta:
        fields = ('type', 'year', 'title', 'length', 'presenter', # talk data
                  'publication', 'page_from', 'page_to', 'editors', 'place' # abstract collection data
        )


class ArticlePosterForm(forms.ModelForm):
    type = forms.ChoiceField(initial = 'POSTER', choices = (('POSTER', _('Poster')),))
    publication = forms.CharField(label=_('Abstract collection'), max_length=50, required=False)

    class Meta:
        fields = ('type', 'year', 'title', 'presenter', # talk data
                  'publication', 'page_from', 'page_to', 'editors', 'place' # abstract collection data
        )
