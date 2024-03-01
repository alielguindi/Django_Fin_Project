from django.urls import path, include
from rest_framework import routers

from .views.plots import StockPlotView, StockPriceGraphView, StockHistView
from .views.stocks_list import StockListView, GetStockData
from .views.portfolio import PortfolioCreate
from .views.about import AboutProject



urlpatterns = [

    path("", StockListView.as_view(), name="stocks-list"),
    path('stocks/<str:ticker>/', GetStockData.as_view(), name='get_stock_data'), 
    path("stock_plots/", StockPriceGraphView.as_view(), name = "stock-plot"), 
    path('plot/<str:stock_ticker>/', StockPlotView.as_view(), name='stock_plot'),
    path('hist/<str:stock_ticker>/', StockHistView.as_view(), name='stock_hist'),
    path('add_investment', PortfolioCreate.as_view(), name ="investment-add" ),
    path('about/', AboutProject.as_view(), name = "about-project"),
]



