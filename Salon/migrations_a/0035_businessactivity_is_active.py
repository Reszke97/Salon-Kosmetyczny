# Generated by Django 3.2.8 on 2023-05-23 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Salon', '0034_alter_employeeavailability_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='businessactivity',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
