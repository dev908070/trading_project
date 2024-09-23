# models.py
from django.db import models

class NiftyData(models.Model):
    date = models.DateField()
    time = models.TimeField()
    tick_price = models.FloatField()
    volume = models.IntegerField()
    open_interest = models.IntegerField()

    def __str__(self):
        return f"{self.date} {self.time} - {self.tick_price}"
