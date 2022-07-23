from django import forms

from .models import RSSItem, Source


class RSSItemForm(forms.ModelForm):

    class Meta:
        model = RSSItem
        fields = (
            'title',
            'pub_date',
            'link'
        )


class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = (
            'title',
            'url',
            'status',
        )
        widgets = {
            'title': forms.TextInput,
        }
