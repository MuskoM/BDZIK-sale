# Generated by Django 3.1.7 on 2021-02-23 16:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0006_auto_20210101_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rezerwacjapokoju',
            name='data_wykonania_rezerwacji',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 23, 17, 23, 47, 485667)),
        ),
        migrations.AlterField(
            model_name='rezerwacjasali',
            name='data_wykonania_rezerwacji',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 23, 17, 23, 47, 483166)),
        ),
    ]