from django.http import HttpResponse
from django.shortcuts import render
from main.search import forms
from .forms import NameForm

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            keyword = form.cleaned_data['your_name']
            get_trend(keyword)
            return render(request, 'search/index.html', {'form': form})



    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'search/index.html', {'form': form})

def get_trend(keyword):

    return forms.trend(keyword)



