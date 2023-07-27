from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'introduction/introduction.html')


def data(request):
    return render(request, 'introduction/a.html')
