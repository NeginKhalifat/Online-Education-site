# Generated by Django 3.0.8 on 2020-07-26 20:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('class', '0007_auto_20200726_1627'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('slug', models.CharField(max_length=30)),
                ('duration', models.DurationField()),
                ('date', models.CharField(max_length=30)),
                ('class_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='class.Class')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RecordMark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('mark', models.FloatField(blank=True)),
                ('participants', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='class.Quiz')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('questions', models.CharField(max_length=200)),
                ('option1', models.CharField(default='', max_length=90)),
                ('option2', models.CharField(default='', max_length=90)),
                ('option3', models.CharField(default='', max_length=90)),
                ('option4', models.CharField(default='', max_length=90)),
                ('answer', models.CharField(default='', max_length=90)),
                ('value', models.FloatField()),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='class.Quiz')),
            ],
        ),
    ]