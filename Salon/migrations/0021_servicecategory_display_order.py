# Generated by Django 3.2.8 on 2022-10-20 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Salon', '0020_auto_20221019_1610'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicecategory',
            name='display_order',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
