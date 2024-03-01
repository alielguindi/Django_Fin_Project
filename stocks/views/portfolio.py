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
from django.views.generic.edit import CreateView



class PortfolioCreate(CreateView) :
    model = Investment
    fields = ["stock","date","share"]
    
    

    def form_valid(self, form) :
        form.instance.user = self.request.user
        return super().form_valid(form)
    


#


class PlotPortfolioEqWeighted(View) :
    def get(self,request ,*args, **kwargs)  :
        qs = Price.objects.values("stock__ticker","date","close_price")
        df = pd.DataFrame(qs)    
        df= df.pivot(index = "date",columns = "stock__ticker", values = "close_price")    
        n = len(df.columns)
        df["equally_weighted"]= (df[df.columns] *1/n).sum(axis =1)
        df["returns"] = df["equally_weighted"].pct_change(1)


        trace = go.Scatter(x= df.index, y = df["equally_weighted"], mode = "lines")
        layout = go.Layout(title ="Close prices for an Equally weighted portfolio", xaxis=dict(title='Date'), yaxis=dict(title='Close Price'))
        fig= go.Figure(data = [trace], layout=layout)
        plot_div = plot(fig, output_type='div', include_plotlyjs=False)

 
    

        return render(request, "stocks/equally_weighted.html", {"plot_div" : plot_div})        



