# Generated by Django 2.0.1 on 2018-01-30 16:40

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('gameinfo', '0004_auto_20180130_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='published_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 1, 30, 16, 40, 3, 580431, tzinfo=utc)),
        ),
    ]