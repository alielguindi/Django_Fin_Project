
from django.db import models
from django.contrib.auth.models import User #Not explicitly defined in models.py
from datetime import date





class Price(models.Model) :
    stock = models.ForeignKey(to = "stocks.Stock", related_name ="prices", on_delete = models.CASCADE)
    # Stock have more than one price. Each Price have only one stock
    close_price = models.DecimalField(max_digits = 10, decimal_places = 2)
    volume = models.IntegerField()
    date = models.DateField()

    def __str__(self) :

        return f'{self.stock} - {self.date} - {self.close_price}'