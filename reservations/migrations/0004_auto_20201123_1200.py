# Generated by Django 3.0.5 on 2020-11-23 11:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0003_auto_20201123_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rezerwacjapokoju',
            name='data_wykonania_rezerwacji',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 23, 12, 0, 37, 843195)),
        ),
        migrations.AlterField(
            model_name='rezerwacjasali',
            name='data_wykonania_rezerwacji',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 23, 12, 0, 37, 841195)),
        ),
    ]