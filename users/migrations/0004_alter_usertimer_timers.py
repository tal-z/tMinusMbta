# Generated by Django 3.2.9 on 2021-11-21 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20211120_2348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertimer',
            name='timers',
            field=models.JSONField(),
        ),
    ]
