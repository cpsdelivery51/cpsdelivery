# Generated by Django 5.0.6 on 2024-09-23 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_remove_profile_firstname_remove_profile_lastname'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='accountType',
            field=models.CharField(choices=[('Rider', 'Rider'), ('Restaurant', 'Restaurant'), ('Nuser', 'Nuser'), ('Nadmin', 'Nadmin')], default='Nuser', max_length=10),
        ),
    ]
