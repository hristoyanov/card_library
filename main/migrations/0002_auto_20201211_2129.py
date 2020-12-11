# Generated by Django 3.1.3 on 2020-12-11 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='hero_class',
            field=models.CharField(blank=True, choices=[('demon_hunter', 'Demon Hunter'), ('druid', 'Druid'), ('hunter', 'Hunter'), ('mage', 'Mage'), ('paladin', 'Paladin'), ('priest', 'Priest'), ('rogue', 'Rogue'), ('shaman', 'Shaman'), ('warlock', 'Warlock'), ('warrior', 'Warrior')], max_length=12),
        ),
    ]
