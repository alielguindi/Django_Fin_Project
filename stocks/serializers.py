from rest_framework import serializers
from stocks.models import Stock


# Serializers define the API representation.
#class StockSerializer(serializers.HyperlinkedModelSerializer):
    #class Meta:
        #model = Stock
        #fields = ['ticker', 'currency']