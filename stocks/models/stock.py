from django.db import models
from django.contrib.auth.models import User #Not explicitly defined in models.py
from datetime import date
from stocks.models.price import Price


#Create your models here.

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
    


