# Generated by Django 3.2.9 on 2021-11-21 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_usertimer_timers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertimer',
            name='timers',
            field=models.CharField(max_length=500),
        ),
    ]
