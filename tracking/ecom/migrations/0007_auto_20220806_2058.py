# Generated by Django 3.0.5 on 2022-08-07 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0006_orders_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='num_order',
            field=models.CharField(max_length=500, null=True),
        ),
    ]