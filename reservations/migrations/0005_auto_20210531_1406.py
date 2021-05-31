# Generated by Django 3.2 on 2021-05-31 12:06

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0004_auto_20210531_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rezerwacjapokoju',
            name='data_wykonania_rezerwacji',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 31, 12, 6, 4, 608845, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='rezerwacjasali',
            name='data_wykonania_rezerwacji',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 31, 12, 6, 4, 607346, tzinfo=utc)),
        ),
    ]
