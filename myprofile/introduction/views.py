from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'introduction/templlate.html')



def skills(request):
    return render(request, 'introduction/skills.html')

def experience(request):
    return render(request, 'introduction/experience.html')



def contact(request):
    return render(request, 'introduction/contact.html')