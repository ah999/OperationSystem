# Generated by Django 3.2 on 2022-06-27 11:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operationreservation', '0003_auto_20220627_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operation',
            name='date',
            field=models.DateField(default=datetime.date(2022, 6, 27)),
        ),
    ]