# Generated by Django 3.2.8 on 2022-08-20 13:10

import Salon.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Salon', '0011_employeeservicerelation'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.ImageField(blank=True, null=True, upload_to=Salon.models.upload_path)),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Salon.employee')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeServiceConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_order', models.IntegerField()),
                ('styles', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Salon.employee')),
                ('employee_image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Salon.employeeimage')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('styles', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='service',
            name='styles',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='EmployeeServiceRelation',
        ),
        migrations.AddField(
            model_name='employeeserviceconfiguration',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Salon.service'),
        ),
        migrations.AddField(
            model_name='service',
            name='service_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Salon.servicecategory'),
        ),
    ]
