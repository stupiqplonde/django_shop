from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context = {
        'title': 'Home',
        'content': 'Home',
    }
    return render(request, 'index.html', context)

def about(request):
    context = {
        'title': 'About page',
        'content': 'About page',
    }
    return render(request, 'about.html', context)
