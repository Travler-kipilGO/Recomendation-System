# Generated by Django 3.2 on 2021-04-25 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Map', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour_spot_rating',
            name='areacode',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
