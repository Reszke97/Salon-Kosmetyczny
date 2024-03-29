# Generated by Django 3.2.8 on 2022-11-13 13:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Salon', '0025_servicecomment'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeCommentSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='employeeserviceconfiguration',
            name='comment_set',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Salon.employeecommentset'),
        ),
        migrations.AddField(
            model_name='servicecomment',
            name='comment_set',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Salon.employeecommentset'),
        ),
    ]
