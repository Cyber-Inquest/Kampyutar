# Generated by Django 4.0.2 on 2022-02-10 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0005_category_discount_subcategory_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='slideshow',
            name='link',
            field=models.CharField(default='default', max_length=200),
        ),
    ]
