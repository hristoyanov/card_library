# Generated by Django 3.1.3 on 2020-12-12 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20201211_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='hero_class',
            field=models.CharField(choices=[('demon_hunter', 'Demon Hunter'), ('druid', 'Druid'), ('hunter', 'Hunter'), ('mage', 'Mage'), ('paladin', 'Paladin'), ('priest', 'Priest'), ('rogue', 'Rogue'), ('shaman', 'Shaman'), ('warlock', 'Warlock'), ('warrior', 'Warrior')], max_length=12),
        ),
    ]