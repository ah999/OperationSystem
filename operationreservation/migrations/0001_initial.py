# Generated by Django 3.2 on 2022-04-09 12:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctor_name', models.CharField(max_length=70)),
                ('patient_id', models.IntegerField()),
                ('date', models.DateField()),
                ('duration', models.FloatField()),
                ('emergency', models.FloatField()),
                ('department_id', models.CharField(max_length=10)),
                ('room_id', models.CharField(max_length=10)),
                ('time_slot', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='OpRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('date', models.DateField()),
                ('operation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='operationreservation.operation')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('capacity', models.IntegerField()),
                ('date', models.DateField()),
                ('operation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='operationreservation.operation')),
            ],
        ),
    ]