# Generated by Django 3.0.5 on 2022-08-01 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0004_orders_num_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='cant',
            field=models.BigIntegerField(null=True),
        ),
    ]