# Generated by Django 3.0.5 on 2020-05-18 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emp', '0076_auto_20200518_1404'),
    ]

    operations = [
        migrations.AddField(
            model_name='student_status',
            name='ename',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='student_status',
            name='jtitle',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='student_status',
            name='semail',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='student_status',
            name='sphno',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='student_status',
            name='comp',
            field=models.CharField(default='', max_length=100),
        ),
    ]
