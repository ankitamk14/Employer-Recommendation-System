# Generated by Django 3.0.5 on 2020-05-01 13:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emp', '0021_auto_20200501_1716'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='rel',
        ),
    ]
