from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


def homepage(request):
    return render(request, 'index.html')

def homepageText(request, str):
    return render(request, 'index.html')
