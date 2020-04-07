from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
import uuid
import boto3

from .models import Instrument, Product, Photo
from .forms import PracticeForm

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'catcollector-fr'

# Create your views here.
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


def assoc_product(request, instrument_id, product_id):
  Instrument.objects.get(id=instrument_id).products.add(product_id)
  return redirect('detail', instrument_id=instrument_id)

def dissoc_product(request, instrument_id, product_id):
    Instrument.objects.get(id=instrument_id).products.remove(product_id)
    return redirect('detail', instrument_id=instrument_id)

def home(request):  
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def instruments_index(request):
    instruments = Instrument.objects.all()
    return render(request, 'instruments/index.html', { 'instruments' : instruments })

def instruments_detail(request, instrument_id):
    instrument = Instrument.objects.get(id=instrument_id)
    products_instrument_doesnt_have = Product.objects.exclude(id__in = instrument.products.all().values_list('id'))
    practice_form = PracticeForm()
    return render(request, 'instruments/detail.html', { 'instrument': instrument, 'practice_form' : practice_form, 'products' : products_instrument_doesnt_have })

def add_practice(request, instrument_id):
    form = PracticeForm(request.POST)
    if form.is_valid():
        new_practice = form.save(commit=False)
        new_practice.instrument_id = instrument_id
        new_practice.save()
    return redirect('detail', instrument_id=instrument_id)

class InstrumentCreate(CreateView):
    model = Instrument
    fields = ['make', 'model', 'year', 'description']
    success_url = '/instruments/'

class InstrumentUpdate(UpdateView):
    model = Instrument
    fields = ['model', 'year', 'description']

class InstrumentDelete(DeleteView):
  model = Instrument
  success_url = '/instruments/'

class ProductList(ListView):
    model = Product

class ProductDetail(DetailView):
    model = Product

class ProductCreate(CreateView):
    model = Product
    fields = ['name']
    success_url = '/products/'

class ProductUpdate(UpdateView):
    model = Product
    fields = ['name']
    success_url = '/products/'

class ProductDelete(DeleteView):
    model = Product
    success_url = '/products/'