# Generated by Django 4.2.1 on 2023-09-19 21:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('animes', '0003_anime_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='anime',
            old_name='order',
            new_name='orden',
        ),
    ]
