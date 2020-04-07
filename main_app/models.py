from django.db import models
from django.urls import reverse

# Create your models here.
class Instrument(models.Model):  
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    description = models.TextField(max_length=250)

    def __str__(self):
        return self.make
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'instrument_id': self.id})
