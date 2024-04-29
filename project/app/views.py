from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

# Create your views here.
def console(request):
    return render(request, 'console.html')


def home(request):
    text = f"<h1>THIS HOMEPAGE</h1>"
    return HttpResponse(text)