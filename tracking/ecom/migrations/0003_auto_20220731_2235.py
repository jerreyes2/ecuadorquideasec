# Generated by Django 3.0.5 on 2022-08-01 03:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0002_auto_20220731_2030'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='send',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='subtotal',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='total',
        ),
        migrations.AddField(
            model_name='orders',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ecom.Product'),
        ),
        migrations.DeleteModel(
            name='Orders_list',
        ),
    ]
