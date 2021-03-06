# Generated by Django 3.0.5 on 2020-05-17 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emp', '0068_remove_contact_stu_student'),
    ]

    operations = [
        migrations.CreateModel(
            name='rate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('rating', models.IntegerField()),
                ('suggestion', models.TextField(max_length=500)),
                ('reply', models.TextField(blank=True, max_length=1000)),
            ],
        ),
    ]
