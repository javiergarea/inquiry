import datetime
import re
from django import forms
from django.core.exceptions import ValidationError

SUBJECT_CHOICES = [
    ('cs', 'Computer Science'),
    ('math', 'Mathematics'),
    ('stat', 'Statistics'),
    ('physics', 'Physics'),
    ('all', 'All'),
]


class BasicSearchForm(forms.Form):
    keywords = forms.CharField(label='', max_length=100)
    subject = forms.CharField(label='', initial='all', widget=forms.Select(choices=SUBJECT_CHOICES))

    def clean(self):
        keywords = self.cleaned_data.get('keywords')
        keywords = re.sub('[^A-Za-z0-9 ]+', '', keywords)
        if not keywords:
            raise ValidationError("You must specify at least one keyword.")


class AdvancedSearchForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100, required=False)
    authors = forms.CharField(label='Authors', max_length=100, required=False)
    abstract = forms.CharField(label='Abstract', max_length=100, required=False)
    content = forms.CharField(label='Content', max_length=100, required=False)
    subject = forms.CharField(label='', initial='all',
                              widget=forms.Select(choices=SUBJECT_CHOICES), required=False)

    def clean(self):
        title = self.cleaned_data.get('title')
        title = re.sub('[^A-Za-z0-9 ]+', '', title)
        authors = self.cleaned_data.get('authors')
        authors = re.sub('[^A-Za-z0-9 ]+', '', authors)
        abstract = self.cleaned_data.get('abstract')
        abstract = re.sub('[^A-Za-z0-9 ]+', '', abstract)
        content = self.cleaned_data.get('content')
        content = re.sub('[^A-Za-z0-9 ]+', '', content)
        if not (title or authors or abstract or content):
            raise ValidationError('You must specify at least one field')
