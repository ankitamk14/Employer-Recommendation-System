# Generated by Django 3.0.5 on 2020-04-29 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emp', '0008_employer_company_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobs',
            name='test_score',
            field=models.FloatField(default=0.0),
        ),
    ]
