'''
Create a function that fetches data from Alpha Vantage

'''

import requests
from django.conf import settings
from .models import Stock, Price
import requests

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
#url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo'
#r = requests.get(url)
#data = r.json()



def fetch_data(symbol) :
    api_key = settings.ALPHA_VINTAGE_API_KEY
    #If we get a stock with that symbol nothing is created
    #created = False 
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}'
    stock, created = Stock.objects.get_or_create(  
        ticker = symbol, defaults={"currency" : "Dollar"}
    )
    
    r = requests.get(url)
    data = r.json()

    time_series = data.get("Time Series (Daily)")
    for date, daily_data in time_series.items() :
        Price.objects.update_or_create(stock = stock,
                         date = date,
                         defaults = {"close_price" : daily_data.get("4. close") , "volume" : daily_data.get("5. volume")}

        )


