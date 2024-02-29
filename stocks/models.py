from django.db import models
from django.contrib.auth.models import User #Not explicitly defined in models.py

from datetime import date

# Create your models here.

# Database I : For the sotck
#Name, ticker, and currency here we have only dollars since we are dealing with American equity 
class Stock(models.Model) :
    ticker = models.CharField(max_length = 12)
    currency = models.CharField(max_length = 10)

    def __str__(self) :
        return f'{self.ticker}'
     
    
    #Getting the last_price for each instance of Stock
    @property
    def last_price(self) -> models.DecimalField | None :
        try :
            last_price = self.prices.latest("date").close_price   #self.related_name.latest(date).close_price
        except Price.DoesNotExist :
            last_price = None 

        return last_price

    @property
    def last_date(self) -> models.DecimalField | None :
        try :
            last_date = self.prices.latest("date").date   #self.related_name.latest(date).close_price
        except Price.DoesNotExist :
            last_date = None 

        return last_date
    
    @property 
    def last_volume(self) -> models.IntegerField | None :
        try :
            last_volume = self.prices.latest("date").volume  #self.related_name.latest(date).close_price
        except Price.DoesNotExist :
            last_volume = None 

        return last_volume
    





class Price(models.Model) :
    stock = models.ForeignKey(Stock, related_name ="prices", on_delete = models.CASCADE)
    # Stock have more than one price. Each Price have only one stock
    close_price = models.DecimalField(max_digits = 10, decimal_places = 2)
    volume = models.IntegerField()
    date = models.DateField()

    def __str__(self) :

        return f'{self.stock} - {self.date} - {self.close_price}'
        






class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



from django.utils import timezone

date = models.DateField(default=timezone.now)


class Investment(models.Model):
    stock = models.ForeignKey(Stock, related_name="investments", on_delete=models.CASCADE)
    #date = models.DateField(default="2023-01-01")
    date = models.DateField(default=timezone.now)
    weight = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Adjusted decimal places
    share = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Adjusted decimal places
    portfolio = models.ForeignKey(Portfolio, related_name="investments", on_delete=models.CASCADE)

    def __str__(self):
        return f'Investment in {self.stock.ticker} on {self.date} with {self.share} shares at weight {self.weight}'


