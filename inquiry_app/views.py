from django.shortcuts import render
from inquiry_app.forms import BasicSearchForm, AdvancedSearchForm
from inquiry_app.services import InquiryService

# Create your views here.


def index(request):
    ctx = {'basicform': BasicSearchForm(),
           'advancedform': AdvancedSearchForm()}
    return render(request, 'index.html', ctx)


def search(request):
    print(request.GET)
    service = InquiryService()
    ctx = service.search_by_keywords(request.GET.get('keywords'))
    cdict = {"title": c for c in ctx}
    return render(request, 'search.html', cdict)


def about(request):
    return render(request, 'about.html')
