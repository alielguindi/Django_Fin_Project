# Generated by Django 5.0.2 on 2024-02-29 16:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(max_length=12)),
                ('currency', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('close_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('volume', models.IntegerField()),
                ('date', models.DateField()),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='stocks.stock')),
            ],
        ),
        migrations.CreateModel(
            name='Investment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('weight', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('share', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('value', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('portfolio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='investments', to='stocks.portfolio')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='investments', to='stocks.stock')),
               
            ],
        ),
    ]
