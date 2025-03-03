# Generated by Django 5.1.4 on 2025-03-03 18:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_entradaproducto_productoentrada'),
    ]

    operations = [
        migrations.CreateModel(
            name='NumeroDeEntradas',
            fields=[
                ('entrada', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='app.entradaproducto')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.proveedor')),
            ],
        ),
        migrations.DeleteModel(
            name='ProductoEntrada',
        ),
    ]
