from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from . import log

# Create your views here.
def console(request):
    logs = log.all_logs
    return render(request, 'console.html', {'logs': logs})


def home(request):
    text = f"<h1>THIS HOMEPAGE</h1>"
    return HttpResponse(text)