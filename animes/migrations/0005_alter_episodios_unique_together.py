# Generated by Django 4.2.1 on 2023-09-25 21:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('animes', '0004_rename_order_anime_orden'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='episodios',
            unique_together={('anime_id', 'numero_episodio')},
        ),
    ]