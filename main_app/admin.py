from django.contrib import admin
from .models import Instrument, Practice, Product, Photo

# Register your models here.
admin.site.register(Instrument)
admin.site.register(Practice)
admin.site.register(Product)
admin.site.register(Photo)


