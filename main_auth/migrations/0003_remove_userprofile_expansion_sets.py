# Generated by Django 3.1.3 on 2020-12-07 13:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_auth', '0002_auto_20201207_1405'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='expansion_sets',
        ),
    ]