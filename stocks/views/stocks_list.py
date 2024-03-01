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


class StockListView(ListView) :
    model = Stock  # Specify the model we want to work with
    template_name = "stocks/stock_list_view.html" # Specify your template name
    context_object_name = "stocks" #Your context name to use in the template





class GetStockData(DetailView):
    model = Stock
    template_name = "stocks/stock_individual.html"
    context_object_name = "stock"

    def get_object(self):
        pk= self.kwargs.get("pk")
        return get_object_or_404(Stock, pk=pk)    
    

      