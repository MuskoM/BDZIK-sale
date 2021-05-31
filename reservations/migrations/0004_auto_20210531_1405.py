# Generated by Django 3.2 on 2021-05-31 12:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0003_auto_20210531_1308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rezerwacjapokoju',
            name='data_wykonania_rezerwacji',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 31, 12, 5, 27, 926087, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='rezerwacjasali',
            name='data_wykonania_rezerwacji',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 31, 12, 5, 27, 924587, tzinfo=utc)),
        ),
    ]