# Generated by Django 4.1.7 on 2023-04-09 13:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset_manage_app', '0002_alter_housekeep_category_alter_housekeep_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='housekeep',
            name='date',
            field=models.DateField(default=datetime.date(2023, 4, 9)),
        ),
    ]
