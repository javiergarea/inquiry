from django import forms
from django.core.exceptions import ValidationError
import datetime

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
        subject = self.cleaned_data.get('subject')
        if not (keywords and subject):
            raise ValidationError("You must specify at least one keyword.")



    def clean(self):
        title = self.cleaned_data.get('title')
        authors = self.cleaned_data.get('authors')
        abstract = self.cleaned_data.get('abstract')
        content = self.cleaned_data.get('content')
        if not (title or authors or abstract or content):
            raise ValidationError("You must specify at least one field")

class AdvancedSearchForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100, required=False)
    authors = forms.CharField(label='Authors', max_length=100, required=False)
    abstract = forms.CharField(label='Abstract', max_length=100, required=False)
    content = forms.CharField(label='Content', max_length=100, required=False)
    subject = forms.CharField(label='', initial='all', widget=forms.Select(choices=SUBJECT_CHOICES), required=False)
    start_date = forms.DateField(initial=(datetime.datetime.now() - datetime.timedelta(days=1*365)), required=False)
    end_date = forms.DateField(initial=datetime.date.today, required=False)

    def clean(self):
        title = self.cleaned_data.get('title')
        authors = self.cleaned_data.get('authors')
        abstract = self.cleaned_data.get('abstract')
        content = self.cleaned_data.get('content')
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        if not (title or authors or abstract or content):
            raise ValidationError('You must specify at least one field')
