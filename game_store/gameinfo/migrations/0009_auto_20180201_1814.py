# Generated by Django 2.0.1 on 2018-02-01 18:14

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('gameinfo', '0008_auto_20180201_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='published_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 1, 18, 14, 20, 110685, tzinfo=utc)),
        ),
    ]
