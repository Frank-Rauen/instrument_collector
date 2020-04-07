from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView


from .models import Instrument, Product 
from .forms import PracticeForm

# Create your views here.
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