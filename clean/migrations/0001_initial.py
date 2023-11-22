# Generated by Django 4.2.6 on 2023-11-16 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clientes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contraparte', models.CharField(choices=[('Cliente', 'Cliente'), ('Proveedor', 'Proveedor')], default='Cliente', max_length=10)),
                ('fecha_transaccion', models.DateField()),
                ('nit', models.CharField(max_length=20)),
                ('nombre', models.CharField(max_length=255)),
                ('ciiu', models.IntegerField()),
                ('valor_transaccion', models.DecimalField(decimal_places=2, max_digits=30)),
                ('pais', models.CharField(max_length=255)),
                ('ciudad', models.CharField(max_length=255)),
                ('departamento', models.CharField(max_length=255)),
                ('funcionario', models.CharField(max_length=255)),
                ('tipo_de_persona', models.CharField(max_length=10)),
                ('medio_de_pago', models.CharField(max_length=20)),
                ('canal_de_distribucion', models.CharField(max_length=255)),
                ('medio_de_venta', models.CharField(max_length=255)),
                ('ano', models.IntegerField(blank=True, null=True)),
                ('mes', models.IntegerField(blank=True, null=True)),
                ('nombre_archivo', models.CharField(blank=True, max_length=255, null=True)),
                ('alarmas', models.CharField(blank=True, max_length=255, null=True)),
                ('Concatenado', models.CharField(blank=True, max_length=255, null=True)),
                ('SinCorr_Ciudad', models.CharField(blank=True, max_length=255, null=True)),
                ('SinCorrespondencia', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Cliente_limpio',
                'verbose_name_plural': 'Cliente_Limpios',
            },
        ),
        migrations.CreateModel(
            name='Contraparte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('Cliente', 'Cliente'), ('Proveedor', 'Proveedor')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Generales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departamento', models.CharField(blank=True, max_length=255, null=True)),
                ('municipio', models.CharField(blank=True, max_length=255, null=True)),
                ('divipola', models.CharField(blank=True, max_length=255, null=True)),
                ('categoria', models.CharField(blank=True, max_length=255, null=True)),
                ('valor_riesgo', models.IntegerField(blank=True, null=True)),
                ('cod_ciiu', models.CharField(blank=True, max_length=255, null=True)),
                ('seccion', models.CharField(blank=True, max_length=255, null=True)),
                ('division', models.CharField(blank=True, max_length=255, null=True)),
                ('grupo', models.CharField(blank=True, max_length=255, null=True)),
                ('descripcion', models.CharField(blank=True, max_length=255, null=True)),
                ('valor', models.FloatField(blank=True, null=True)),
                ('calificacion', models.CharField(blank=True, max_length=255, null=True)),
                ('frecuencia', models.CharField(blank=True, max_length=255, null=True)),
                ('indicador', models.CharField(blank=True, max_length=255, null=True)),
                ('val_promedio_transaccion', models.FloatField(blank=True, null=True)),
                ('mayor', models.FloatField(blank=True, null=True)),
                ('menor', models.FloatField(blank=True, null=True)),
                ('toma', models.FloatField(blank=True, null=True)),
                ('ciuu_porcentaje', models.FloatField(blank=True, null=True)),
                ('jurisdiccion_porcentaje', models.FloatField(blank=True, null=True)),
                ('tipo_pers_porcentaje', models.FloatField(blank=True, null=True)),
                ('medio_pago_porcentaje', models.FloatField(blank=True, null=True)),
                ('va_porcentaje', models.FloatField(blank=True, null=True)),
                ('transacciones_entero', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'general',
                'verbose_name_plural': 'generales',
            },
        ),
        migrations.CreateModel(
            name='Proveedores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contraparte', models.CharField(choices=[('Cliente', 'Cliente'), ('Proveedor', 'Proveedor')], default='Proveedor', max_length=10)),
                ('fecha_transaccion', models.DateField()),
                ('nit', models.CharField(max_length=20)),
                ('nombre', models.CharField(max_length=255)),
                ('ciiu', models.IntegerField()),
                ('detalle', models.CharField(max_length=255)),
                ('valor_transaccion', models.DecimalField(decimal_places=2, max_digits=30)),
                ('pais', models.CharField(max_length=255)),
                ('ciudad', models.CharField(max_length=255)),
                ('departamento', models.CharField(max_length=255)),
                ('ano', models.IntegerField(blank=True, null=True)),
                ('mes', models.IntegerField(blank=True, null=True)),
                ('nombre_archivo', models.CharField(blank=True, max_length=255, null=True)),
                ('tipo_de_persona', models.CharField(max_length=10)),
                ('medio_de_pago', models.CharField(max_length=20)),
                ('alarmas', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'P_limpio',
                'verbose_name_plural': 'P_Limpios',
            },
        ),
    ]
