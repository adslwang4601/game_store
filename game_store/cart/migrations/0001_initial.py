# Generated by Django 2.0.1 on 2018-02-02 18:55

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Profile', '0001_initial'),
        ('gameinfo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('order_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('payment_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('paid', models.CharField(default=False, max_length=20)),
                ('total', models.DecimalField(decimal_places=2, max_digits=6)),
                ('_games', models.ManyToManyField(blank=True, default=None, to='gameinfo.Game')),
                ('_player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Profile.User_Profile')),
            ],
            options={
                'ordering': ('-order_time',),
            },
        ),
    ]