from django import forms

from .models import RSSItem, Task


class RSSItemForm(forms.ModelForm):

    class Meta:
        model = RSSItem
        fields = (
            'title',
            'pub_date',
            'link'
        )


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = (
            'title',
            'url',
            'status',
        )
        widgets = {
            'title': forms.TextInput,
        }
