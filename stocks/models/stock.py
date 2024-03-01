from django.db import models
from django.contrib.auth.models import User #Not explicitly defined in models.py
from datetime import date
from stocks.models.price import Price
import requests


#Create your models here.

# Database I : For the sotck
#Name, ticker, and currency here we have only dollars since we are dealing with American equity 
class Stock(models.Model) :
    ticker = models.CharField(max_length = 12)
    currency = models.CharField(max_length = 10)

    def __str__(self) :
        return f'{self.ticker}'

     


    @property
    def last_price_details(self):
        # Initialize default values for price details
        last_price_details = {
            'last_price': None,
            'last_date': None,
            'last_volume': None
        }

        try:
            # Fetch the latest Price instance related to this Stock
            latest_price = self.prices.latest("date")

            # Update the details using the latest Price instance
            last_price_details.update({
                'last_price': latest_price.close_price,
                'last_date': latest_price.date,
                'last_volume': latest_price.volume,
            })
        except Price.DoesNotExist:
            # If no Price instance exists, the defaults remain None
            pass

        return last_price_details
    

    @classmethod
    def fetch_data(self):
        
        api_key = settings.ALPHA_VINTAGE_API_KEY
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={self.ticker}&apikey={api_key}'

        r = requests.get(url)
        data = r.json()

        time_series = data.get("Time Series (Daily)")
        if time_series:
            for date, daily_data in time_series.items():
                Price.objects.update_or_create(
                    stock=self,
                    date=date,
                    defaults={
                        "close_price": daily_data.get("4. close"),
                        "volume": daily_data.get("5. volume")
                    }
                )




