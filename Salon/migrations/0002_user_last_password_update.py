# Generated by Django 3.2.8 on 2021-12-20 11:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Salon', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_password_update',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
