# Generated by Django 4.0.2 on 2022-04-10 08:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0003_alter_vendorappleproducts_brand_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendorappleproducts',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 10, 13, 45, 9, 192361)),
        ),
        migrations.AlterField(
            model_name='vendorcomponentsproducts',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 10, 13, 45, 9, 192361)),
        ),
        migrations.AlterField(
            model_name='vendordesktopsproducts',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 10, 13, 45, 9, 192361)),
        ),
        migrations.AlterField(
            model_name='vendorlaptopproducts',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 10, 13, 45, 9, 192361)),
        ),
    ]
