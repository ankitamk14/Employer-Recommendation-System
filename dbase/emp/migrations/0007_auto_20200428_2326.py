# Generated by Django 3.0.5 on 2020-04-28 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emp', '0006_student_jobs'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='jobs',
        ),
        migrations.CreateModel(
            name='appliedjobs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jobs', models.ManyToManyField(to='emp.jobs')),
                ('student', models.ManyToManyField(to='emp.student')),
            ],
        ),
    ]
