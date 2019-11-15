from django import forms

SUBJECT_CHOICES = [
    ('cs', 'Computer Science'),
    ('math', 'Mathematics'),
    ('stat', 'Statistics'),
    ('physics', 'Physics'),
    ('', 'All'),
    ]

class BasicSearchForm(forms.Form):
    keywords = forms.CharField(label="", max_length=100)
    subject = forms.CharField(label='', initial='', widget=forms.Select(choices=SUBJECT_CHOICES))

class AdvancedSearchForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100, required=False)
    authors = forms.CharField(label='Authors', max_length=100, required=False)
    subject = forms.CharField(label='Subject', max_length=100, required=False)
    abstract = forms.CharField(label='Abstract', max_length=100, required=False)
    content = forms.CharField(label='Content', max_length=100, required=False)
