# Generated by Django 5.1.4 on 2024-12-17 18:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_remove_producto_parametros_producto_grupo_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='producto',
            old_name='nombre',
            new_name='nombre_producto',
        ),
    ]
