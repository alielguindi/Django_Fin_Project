from django.db import models
from django.contrib.auth.models import User #Not explicitly defined in models.py

from datetime import date

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
