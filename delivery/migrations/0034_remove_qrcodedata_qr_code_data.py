# Generated by Django 5.0.6 on 2025-03-05 15:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0033_qrcodedata'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='qrcodedata',
            name='qr_code_data',
        ),
    ]
