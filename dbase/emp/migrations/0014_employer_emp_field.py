# Generated by Django 3.0.5 on 2020-04-30 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emp', '0013_employer_emp_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='employer',
            name='emp_field',
            field=models.CharField(default=' ', max_length=50),
        ),
    ]
