# Generated by Django 4.0.2 on 2023-04-06 12:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0005_alter_vendorappleproducts_date_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendorappleproducts',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 6, 18, 41, 9, 81587)),
        ),
        migrations.AlterField(
            model_name='vendorcomponentsproducts',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 6, 18, 41, 9, 81587)),
        ),
        migrations.AlterField(
            model_name='vendordesktopsproducts',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 6, 18, 41, 9, 81587)),
        ),
        migrations.AlterField(
            model_name='vendorlaptopproducts',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 6, 18, 41, 9, 81587)),
        ),
        migrations.AlterField(
            model_name='vendororder',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 6, 18, 41, 9, 81587)),
        ),
        migrations.AlterField(
            model_name='vendorsold',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 6, 18, 41, 9, 81587)),
        ),
    ]
