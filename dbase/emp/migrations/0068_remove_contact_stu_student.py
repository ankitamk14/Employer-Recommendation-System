# Generated by Django 3.0.5 on 2020-05-16 09:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emp', '0067_contact_stu_student'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact_stu',
            name='student',
        ),
    ]
