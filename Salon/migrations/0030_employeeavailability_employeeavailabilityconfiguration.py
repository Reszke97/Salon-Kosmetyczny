# Generated by Django 3.2.8 on 2023-04-17 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Salon', '0029_businessactivity_about'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeAvailabilityConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_weeks_for_registration', models.IntegerField()),
                ('min_time_for_registration', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Salon.employee')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeAvailability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=255)),
                ('is_free', models.BooleanField(default=False)),
                ('is_holiday', models.BooleanField(default=False)),
                ('is_default', models.BooleanField(default=False)),
                ('weekday', models.CharField(max_length=255)),
                ('start_time', models.CharField(max_length=255)),
                ('end_time', models.CharField(max_length=255)),
                ('is_break', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('availability_config', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Salon.employeeavailabilityconfiguration')),
            ],
        ),
    ]
