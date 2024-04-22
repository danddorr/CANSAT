# Generated by Django 4.2.2 on 2024-04-09 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_rename_datetime_realtimedata_date_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='realtimedata',
            name='humidity',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='realtimedata',
            name='pressure',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='realtimedata',
            name='temperature',
            field=models.FloatField(default=0),
        ),
    ]