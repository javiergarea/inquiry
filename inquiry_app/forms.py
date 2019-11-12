from django import forms


class BasicSearchForm(forms.Form):
    keywords = forms.CharField(label="", initial="language models", max_length=100)


class AdvancedSearchForm(forms.Form):
    title = forms.CharField(label='Title', max_length=100, required=False)
    authors = forms.CharField(label='Authors', max_length=100, required=False)
    subject = forms.CharField(label='Subject', max_length=100, required=False)
    abstract = forms.CharField(label='Abstract', max_length=100, required=False)
    content = forms.CharField(label='Content', max_length=100, required=False)
