# Generated by Django 4.2.8 on 2023-12-21 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0002_remove_cart_uuid_cart_cart_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='cart_id',
            field=models.CharField(editable=False, max_length=200, unique=True),
        ),
    ]