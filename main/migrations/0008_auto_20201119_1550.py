# Generated by Django 3.1.3 on 2020-11-19 13:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_expansionset_date_added'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expansionset',
            old_name='date_added',
            new_name='release_date',
        ),
    ]