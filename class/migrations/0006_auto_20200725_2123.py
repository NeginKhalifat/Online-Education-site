# Generated by Django 3.0.8 on 2020-07-25 16:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('class', '0005_auto_20200725_2019'),
    ]

    operations = [
        migrations.RenameField(
            model_name='class',
            old_name='students',
            new_name='teams',
        ),
    ]