from django.shortcuts import render
from inquiry_app.forms import BasicSearchForm, AdvancedSearchForm

# Create your views here.
def index(request):
    ctx = {'basicform': BasicSearchForm(), 'advancedform': AdvancedSearchForm()}
    return render(request, 'index.html', ctx)

def search(request):
    print(request.GET)
    ctx = {}
    return render(request, 'search.html', ctx)

def about(request):
    return render(request, 'about.html')
