# Generated by Django 3.1.7 on 2021-10-16 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0011_auto_20211016_1244'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shippingprice',
            field=models.PositiveIntegerField(default=100),
        ),
    ]
