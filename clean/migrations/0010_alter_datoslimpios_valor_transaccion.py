# Generated by Django 4.2.6 on 2023-10-25 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clean', '0009_remove_datoslimpios_contraparte'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datoslimpios',
            name='valor_transaccion',
            field=models.DecimalField(decimal_places=2, max_digits=30),
        ),
    ]