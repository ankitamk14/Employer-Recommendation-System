# Generated by Django 3.0.5 on 2020-05-01 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emp', '0026_auto_20200501_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appliedjobs',
            name='jobs',
            field=models.ManyToManyField(null=True, to='emp.jobs'),
        ),
        migrations.AlterField(
            model_name='appliedjobs',
            name='student',
            field=models.ManyToManyField(null=True, to='emp.student'),
        ),
    ]
