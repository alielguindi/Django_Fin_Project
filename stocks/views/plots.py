'''
py File that groupy all plots views

'''
from typing import Any
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
#from stocks.models import Stock, Price, Portfolio, Investment
from stocks.models.stock import Stock
from stocks.models.price import Price
from stocks.models.portfolio import Portfolio
from stocks.models.investment import Investment
from django.views.generic import View

import plotly.graph_objs as go
from plotly.offline import plot
import pandas as pd
from django.shortcuts import render, get_object_or_404
#from .forms import InvestmentForm
from django.views.generic import ListView, DetailView, CreateView



class StockPlotView(View): #Line plot for a given stock
    def get(self, request, pk):
        stock = get_object_or_404(Stock, pk=pk)
        
        prices = Price.objects.filter(stock=stock).order_by('date').values('date', 'close_price')
        df = pd.DataFrame(list(prices))
        
        if not df.empty:
            trace = go.Scatter(x=df['date'], y=df['close_price'], mode="lines")
            layout = go.Layout(title=f'Close Prices for over Time', xaxis=dict(title='Date'), yaxis=dict(title='Close Price'))
            fig = go.Figure(data=[trace], layout=layout)
            plot_div = plot(fig, output_type='div', include_plotlyjs=False)
            mean_price = df['close_price'].mean()
            median_price = df['close_price'].median()
            #std_dev = df['close_price'].std()
            max_price = df['close_price'].max()
            min_price = df['close_price'].min()


             # Add statistics to the context
            context = {
                "plot_div": plot_div,
                "mean_price": mean_price,
                "median_price": median_price,
                #"std_dev": std_dev,
                "max_price": max_price,
                "min_price": min_price,
            }
            return render(request, "stocks/individual_stock_plot.html", context)
        else:
            # Handle case where there are no prices available for the stock
            return render(request, "stocks/individual_stock_plot.html", {"error": "No price data available for this stock."})
        


class StockPriceGraphView(View) :#Line plot for all stocks
    def get(self,request, *args,**kwargs):
        list_traces = []
        qs = Price.objects.values("stock__ticker", "close_price", "date").order_by("date")
        df = pd.DataFrame(qs) 
        df = df.pivot(index = "date", columns= "stock__ticker", values = "close_price")
        for col in df.columns  :
            trace = go.Scatter(x= df[col].index, y= df[col].values, name = col)
            list_traces.append(trace)  
        
        layout = go.Layout(title=f'Close Prices for all the tickers over Time', xaxis=dict(title='Date'), yaxis=dict(title='Close Price'))
        fig = go.Figure(data=list_traces, layout=layout)
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)

        return render(request, "stocks/stock_plot.html", context = {"plot_div" : plot_div})   


class StockHistView(View) : #Histogram for each of the stocks
    def get(self,request,pk) :
        stock = get_object_or_404(Stock, pk=pk) # __str__
        qs = Price.objects.filter(stock__ticker = stock).order_by("date").values("date","volume")
        df = pd.DataFrame(qs)
        if not df.empty :
            trace = go.Histogram(x = df["volume"], histnorm='probability')
            layout = go.Layout(title= f'Histogram for {stock} volume over Time')
            fig = go.Figure(data=[trace], layout=layout)
            plot_div = plot(fig, output_type="div", include_plotlyjs=False)

            return render(request, "stocks/individual_stock_hist.html", {"plot_div" : plot_div})
        
        else :
            return render(request, "stocks/individual_stock_hist.html", {"error" : "No price date available for this stock"})