# Generated by Django 3.1.7 on 2021-03-01 08:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0013_auto_20210301_0943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rezerwacjapokoju',
            name='data_wykonania_rezerwacji',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 1, 9, 53, 51, 22389)),
        ),
        migrations.AlterField(
            model_name='rezerwacjasali',
            name='data_wykonania_rezerwacji',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 1, 9, 53, 51, 20387)),
        ),
    ]
