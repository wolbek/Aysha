# Generated by Django 3.1.7 on 2021-10-23 18:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_remove_customer_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='firstname',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='lastname',
        ),
    ]
