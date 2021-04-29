# Generated by Django 3.2 on 2021-04-28 21:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('emp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='emp.course'),
        ),
        migrations.AlterField(
            model_name='student',
            name='degree',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='emp.degree'),
        ),
    ]
