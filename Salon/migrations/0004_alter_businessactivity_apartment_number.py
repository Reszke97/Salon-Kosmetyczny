# Generated by Django 3.2.8 on 2023-07-14 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Salon', '0003_servicecategory_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessactivity',
            name='apartment_number',
            field=models.CharField(default='', max_length=45),
        ),
    ]