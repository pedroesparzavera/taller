# Generated by Django 5.1 on 2024-11-20 08:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0005_alter_producto_descripcion_alter_producto_imagen'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('tfno', models.CharField(blank=True, max_length=20)),
                ('pais', models.CharField(blank=True, max_length=200)),
                ('region', models.CharField(blank=True, max_length=20)),
                ('ciu', models.CharField(blank=True, max_length=20)),
                ('fecha_nac', models.DateField(blank=True, max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]