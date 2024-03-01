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


class AboutProject(View) :
    def get(self,request, *args,**kwargs) :
        return render(request, "stocks/about.html")
