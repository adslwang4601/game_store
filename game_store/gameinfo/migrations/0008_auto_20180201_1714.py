# Generated by Django 2.0.1 on 2018-02-01 17:14

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('gameinfo', '0007_auto_20180201_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='published_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 1, 17, 14, 47, 390543, tzinfo=utc)),
        ),
    ]
