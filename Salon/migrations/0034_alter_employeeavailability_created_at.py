# Generated by Django 3.2.8 on 2023-05-12 14:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Salon', '0033_alter_employeeavailability_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeavailability',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
