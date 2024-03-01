from django.urls import path, include
from rest_framework import routers

from .views import StockListView, GetStockData, StockPlotView, StockPriceGraphView, StockHistView, PortfolioCreate, AboutProject


urlpatterns = [

    path("", StockListView.as_view(), name="stocks-list"),
    path('stocks/<str:ticker>/', GetStockData.as_view(), name='get_stock_data'), 
    path("stock_plots/", StockPriceGraphView.as_view(), name = "stock-plot"), 
    path('plot/<str:stock_ticker>/', StockPlotView.as_view(), name='stock_plot'),
    path('hist/<str:stock_ticker>/', StockHistView.as_view(), name='stock_hist'),
    path('add_investment', PortfolioCreate.as_view(), name ="investment-add" ),
    path('about/', AboutProject.as_view(), name = "about-project"),


    # path('add-investment/', views.AddInvestment.as_view(), name='add-investment'),
]



