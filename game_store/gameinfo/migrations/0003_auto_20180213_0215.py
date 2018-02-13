# Generated by Django 2.0 on 2018-02-13 00:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gameinfo', '0002_auto_20180202_2117'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='url',
            field=models.URLField(default='', unique=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='published_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
