# Generated by Django 3.2.8 on 2022-10-26 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Salon', '0023_auto_20221021_1618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='display_order',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
