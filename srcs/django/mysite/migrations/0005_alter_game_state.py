# Generated by Django 3.2.25 on 2024-09-23 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0004_alter_game_date_time_end'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='state',
            field=models.CharField(default=None, max_length=5),
        ),
    ]
