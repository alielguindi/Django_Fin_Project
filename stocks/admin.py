from django.contrib import admin
from stocks.models import Stock, Price, Portfolio, Investment

# Register your models here.

admin.site.register(Stock)
admin.site.register(Price)
admin.site.register(Portfolio)
admin.site.register(Investment)

