# Generated by Django 3.2 on 2022-07-01 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operationreservation', '0008_auto_20220701_1009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(max_length=20),
        ),
    ]
