# Generated by Django 4.0.2 on 2022-04-06 06:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0041_alter_appleproducts_date_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appleproducts',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 6, 12, 10, 59, 563162)),
        ),
        migrations.AlterField(
            model_name='componentsproducts',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 6, 12, 10, 59, 564159)),
        ),
        migrations.AlterField(
            model_name='desktopsproducts',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 6, 12, 10, 59, 563162)),
        ),
        migrations.AlterField(
            model_name='laptopproducts',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 6, 12, 10, 59, 562165)),
        ),
    ]
