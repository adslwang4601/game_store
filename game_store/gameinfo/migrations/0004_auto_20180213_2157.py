# Generated by Django 2.0.1 on 2018-02-13 21:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gameinfo', '0003_auto_20180213_0215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='publisher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Profile.User_Profile'),
        ),
        migrations.AlterField(
            model_name='game_sale',
            name='buyer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Profile.User_Profile'),
        ),
        migrations.AlterField(
            model_name='game_score',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Profile.User_Profile'),
        ),
    ]