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
            return HttpResponse(forms.trend(keyword))




    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'search/index.html', {'form': form})



