# Generated by Django 4.2.1 on 2023-11-02 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_usuarios_groups_usuarios_is_superuser_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuarios',
            name='password',
            field=models.CharField(max_length=128),
        ),
    ]
