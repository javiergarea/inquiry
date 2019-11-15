from django.shortcuts import render
from inquiry_app.forms import BasicSearchForm, AdvancedSearchForm
from inquiry_app.services import InquiryService
from django.core.exceptions import ValidationError

# Create your views here.


def index(request):
    ctx = {'basicform': BasicSearchForm(),
           'advancedform': AdvancedSearchForm()}
    return render(request, 'index.html', ctx)

def search(request):
    service = InquiryService()
    keywords = request.GET.get('keywords')

    if request.method == 'GET':
        if keywords:
            basic_form = BasicSearchForm(request.GET)
            if basic_form.is_valid():
                result = service.search_by_keywords(basic_form.cleaned_data.get('keywords'),
                                                    basic_form.cleaned_data.get('subject'))
            else:
                return render(request, 'index.html', {'basicform':basic_form,
                                                      'advancedform':AdvancedSearchForm()})
        else:
            adv_form = AdvancedSearchForm(request.GET)
            if adv_form.is_valid():
                title = adv_form.cleaned_data.get('title')
                authors = adv_form.cleaned_data.get('authors')
                abstract = adv_form.cleaned_data.get('abstract')
                content = adv_form.cleaned_data.get('content')
                subject = adv_form.cleaned_data.get('subject')
                result = service.search_by_fields(title, authors, abstract, content, subject)
            else:
                return render(request, 'index.html', {'advancedform':adv_form,
                                                      'basicform': BasicSearchForm()})
        ctx = {"data": result}
        return render(request, 'search.html', ctx)
    else:
        return render(request, 'index.html', {'basicform':basic_form, 'advancedform':adv_form})


def about(request):
    return render(request, 'about.html')
