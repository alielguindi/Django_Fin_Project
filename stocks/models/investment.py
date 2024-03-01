from django.db import models
from django.contrib.auth.models import User #Not explicitly defined in models.py
from datetime import date
from stocks.models.stock import Stock
from stocks.models.portfolio import Portfolio

class Investment(models.Model):
    stock = models.ForeignKey(to = "stocks.Stock", related_name="investments", on_delete=models.CASCADE)
    date = models.DateField()
    weight = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Adjusted decimal places
    share = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Adjusted decimal places
    portfolio = models.ForeignKey("stocks.Portfolio", related_name="investments", on_delete=models.CASCADE)

    def __str__(self):
        return f'Investment in {self.stock.ticker} on {self.date} with {self.share} shares at weight {self.weight}'