from django.shortcuts import render
from django.http import HttpResponse

from .models import Instrument, instruments

# Create your views here.
def home(request):
    return render(request, 'base.html')

def about(request):
    return render(request, 'about.html')

def instruments_index(request):
      return render(request, 'instruments/index.html', { 'instruments' : instruments })