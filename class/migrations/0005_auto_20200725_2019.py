# Generated by Django 3.0.8 on 2020-07-25 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('class', '0004_team_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='date',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='class',
            name='duration',
            field=models.CharField(max_length=30),
        ),
    ]
