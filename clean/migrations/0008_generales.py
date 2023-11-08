# Generated by Django 4.2.6 on 2023-11-08 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clean', '0007_proveedores_alarmas'),
    ]

    operations = [
        migrations.CreateModel(
            name='Generales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departamento', models.CharField(max_length=255)),
                ('municipio', models.CharField(max_length=255)),
                ('divipola', models.CharField(max_length=255)),
                ('categoria', models.CharField(max_length=255)),
                ('valor_riesgo', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
