# Generated by Django 4.2.1 on 2023-11-29 22:48

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('relaciones', '0006_alter_usuarios_animes_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='vizualicion_episodios_usuario',
            name='fecha_agregado',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
