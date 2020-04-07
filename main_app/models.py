from django.db import models
from django.urls import reverse
from datetime import date

from django.contrib.auth.models import User
# Create your models here.
PRACTICES = (
    ('M', 'Morning'),
    ('N', 'Noon'),
    ('K', 'Night')
)

class Product(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Instrument(models.Model):  
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    description = models.TextField(max_length=250)
    products = models.ManyToManyField(Product)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.make
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'instrument_id': self.id})

class Practice(models.Model):
    date = models.DateField('practice time')
    practice = models.CharField(
        max_length = 1,
        choices = PRACTICES,
        default = PRACTICES[0][0]
    ) 

    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_practice_display()} on {self.date}"  
    
    class Meta:
        ordering = ['-date']

class Photo(models.Model):
    url = models.CharField(max_length=200)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for instrument_id: {self.instrument_id} @{self.url}"
