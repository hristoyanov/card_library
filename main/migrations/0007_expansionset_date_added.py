# Generated by Django 3.1.3 on 2020-11-19 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20201117_1633'),
    ]

    operations = [
        migrations.AddField(
            model_name='expansionset',
            name='date_added',
            field=models.DateField(blank=True, null=True),
        ),
    ]
