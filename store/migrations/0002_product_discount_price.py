# Generated by Django 4.2.8 on 2023-12-18 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discount_price',
            field=models.IntegerField(default=0),
        ),
    ]