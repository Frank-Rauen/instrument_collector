from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

import uuid
import boto3

from .models import Instrument, Product, Photo
from .forms import PracticeForm

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'catcollector-fr'

# Create your views here.
@login_required
def add_photo(request, instrument_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
        
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, instrument_id=instrument_id)
            photo.save()
        
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', instrument_id=instrument_id)

@login_required
def assoc_product(request, instrument_id, product_id):
  Instrument.objects.get(id=instrument_id).products.add(product_id)
  return redirect('detail', instrument_id=instrument_id)

@login_required
def dissoc_product(request, instrument_id, product_id):
    Instrument.objects.get(id=instrument_id).products.remove(product_id)
    return redirect('detail', instrument_id=instrument_id)

def home(request):  
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def instruments_index(request):
    instruments = Instrument.objects.filter(user=request.user)
    return render(request, 'instruments/index.html', { 'instruments' : instruments })

@login_required
def instruments_detail(request, instrument_id):
    instrument = Instrument.objects.get(id=instrument_id)
    products_instrument_doesnt_have = Product.objects.exclude(id__in = instrument.products.all().values_list('id'))
    practice_form = PracticeForm()
    return render(request, 'instruments/detail.html', { 'instrument': instrument, 'practice_form' : practice_form, 'products' : products_instrument_doesnt_have })

@login_required
def add_practice(request, instrument_id):
    form = PracticeForm(request.POST)
    if form.is_valid():
        new_practice = form.save(commit=False)
        new_practice.instrument_id = instrument_id
        new_practice.save()
    return redirect('detail', instrument_id=instrument_id)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid Sign Up. Try Again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

class InstrumentCreate(LoginRequiredMixin, CreateView):
    model = Instrument
    fields = ['make', 'model', 'year', 'description']
    success_url = '/instruments/'

    def form_valid(self, form):
        form.instance.user = self.request.user 
        return super().form_valid(form)

class InstrumentUpdate(LoginRequiredMixin, UpdateView):
    model = Instrument
    fields = ['model', 'year', 'description']

class InstrumentDelete(LoginRequiredMixin, DeleteView):
  model = Instrument
  success_url = '/instruments/'

class ProductList(LoginRequiredMixin, ListView):
    model = Product

class ProductDetail(LoginRequiredMixin, DetailView):
    model = Product

class ProductCreate(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['name']
    success_url = '/products/'

class ProductUpdate(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ['name']
    success_url = '/products/'

class ProductDelete(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = '/products/'