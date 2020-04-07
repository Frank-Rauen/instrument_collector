from django.contrib import admin
from .models import Instrument, Practice, Product

# Register your models here.
admin.site.register(Instrument)
admin.site.register(Practice)
admin.site.register(Product)

