# Generated by Django 5.0.6 on 2024-10-07 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0013_cartrestaurant_cartitemrestaurant_restaurantorder_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartrestaurant',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
