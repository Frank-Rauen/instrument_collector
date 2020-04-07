from django.db import models

# Create your models here.
class Instrument:  
  def __init__(self, make, model, year, description):
    self.make = make
    self.model = model
    self.year = year
    self.description = description

instruments = [
    Instrument('Ibanez', 'RG500', 2007, '6 String Shred Machine'),
    Instrument('Gibson', 'Les Paul', 2007, '6 String Shred Machine'),
    Instrument('Fender', 'Stratocaster', 2007, '6 String Shred Machine'),
    ]