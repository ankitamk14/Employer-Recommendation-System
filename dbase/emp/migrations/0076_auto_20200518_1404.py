# Generated by Django 3.0.5 on 2020-05-18 08:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emp', '0075_student_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student_status',
            old_name='status',
            new_name='statu',
        ),
    ]
