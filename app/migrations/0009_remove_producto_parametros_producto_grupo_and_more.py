# Generated by Django 5.1.4 on 2024-12-17 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_producto_parametros'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='parametros',
        ),
        migrations.AddField(
            model_name='producto',
            name='grupo',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='producto',
            name='linea',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='producto',
            name='unidad',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
