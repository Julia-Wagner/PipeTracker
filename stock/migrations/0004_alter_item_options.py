# Generated by Django 4.2.8 on 2024-01-29 19:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0003_alter_item_matchcode'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['matchcode']},
        ),
    ]
