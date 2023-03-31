# Generated by Django 4.0.2 on 2022-03-03 07:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0023_productspecification'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='product_specification_list',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='productspecificationlist', to='admin_panel.category'),
        ),
        migrations.CreateModel(
            name='ProductSpecificationList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=1000)),
                ('product_specification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_panel.productspecification')),
            ],
            options={
                'db_table': 'ProductSpecificationList',
            },
        ),
    ]
