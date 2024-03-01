from typing import Any
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
#from stocks.models import Stock, Price, Portfolio, Investment
from stocks.models.stock import Stock
from stocks.models.price import Price
from stocks.models.portfolio import Portfolio
from stocks.models.investment import Investment
from django.db.models import Prefetch
from django.views.generic import View
from .models import Stock, Price
import plotly.graph_objs as go
from plotly.offline import plot
import pandas as pd
from django.shortcuts import render, get_object_or_404
#from .forms import InvestmentForm
from django.views.generic import ListView, DetailView, CreateView

#Django offers a variety of generic class-based views for common web development tasks. 
#Each is designed to handle specific types of operations, such as displaying a single object, handling forms, 
#or editing objects. Here are some of the commonly used generic class-based views:

#Check https://docs.djangoproject.com/en/5.0/topics/class-based-views/generic-display/ for class based views where you can instantiate from


class StockListView(ListView) :
    model = Stock  # Specify the model we want to work with
    template_name = "stocks/stock_list_view.html" # Specify your template name
    context_object_name = "stocks" #Your context name to use in the template
    


class GetStockData(DetailView):
    model = Stock
    template_name = "stocks/stock_individual.html"
    context_object_name = "stock"

    def get_object(self):
        ticker = self.kwargs.get("ticker")
        return get_object_or_404(Stock, ticker=ticker)



class StockPlotView(View): #Line plot for a given stock
    def get(self, request, stock_ticker):
        stock = get_object_or_404(Stock, ticker=stock_ticker)
        prices = Price.objects.filter(stock__ticker=stock).order_by('date').values('date', 'close_price')
        df = pd.DataFrame(list(prices))
        
        if not df.empty:
            trace = go.Scatter(x=df['date'], y=df['close_price'], mode="lines", name=stock_ticker)
            layout = go.Layout(title=f'Close Prices for {stock_ticker} over Time', xaxis=dict(title='Date'), yaxis=dict(title='Close Price'))
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
    def get(self,request,stock_ticker) :
        stock = get_object_or_404(Stock, ticker = stock_ticker) # __str__
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



class PortfolioCreate(CreateView) :
    model = Investment
    fields = ["stock","date","share"]
    
    

    def form_valid(self, form) :
        form.instance.user = self.request.user
        return super().form_valid(form)
    




class AboutProject(View) :
    def get(self,request, *args,**kwargs) :
        return render(request, "stocks/about.html")





#We should be having a view for each of the portfolios :
# 1) Name
# 2) Date of creation
# 3) It's total value
#-> This will be put in a seperate redirection.

#Wrapping up pour demain : 
# finir le souci de error de date field
# then finishing the form and then add it to a view to visualize this  : Name, Date of starting investing, total value of the portfolio. could be rediorected from
#the main page 
