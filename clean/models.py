from django.db import models

class Contraparte(models.Model):
    TIPOS_CONTRAPARTE = [
        ('Cliente', 'Cliente'),
        ('Proveedor', 'Proveedor'),
    ]

    tipo = models.CharField(max_length=10, choices=TIPOS_CONTRAPARTE)


class Clientes(models.Model):
    contraparte = models.CharField(max_length=10, choices=Contraparte.TIPOS_CONTRAPARTE, default='Cliente')
    fecha_transaccion = models.DateField()
    nit = models.CharField(max_length=20)
    nombre = models.CharField(max_length=255)
    ciiu = models.IntegerField()
    valor_transaccion = models.DecimalField(max_digits=30, decimal_places=2)
    pais = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=255)
    departamento = models.CharField(max_length=255)
    funcionario = models.CharField(max_length=255)
    tipo_de_persona = models.CharField(max_length=10)
    medio_de_pago = models.CharField(max_length=20)
    canal_de_distribucion = models.CharField(max_length=255)
    medio_de_venta = models.CharField(max_length=255)
    ano = models.IntegerField(blank=True, null=True)
    mes = models.IntegerField(blank=True, null=True)
    nombre_archivo = models.CharField(max_length=255, null=True, blank=True)
    alarmas = models.CharField(max_length=255, null=True, blank=True)
    Concatenado = models.CharField(max_length=255, null=True, blank=True)
    SinCorr_Ciudad = models.CharField(max_length=255, null=True, blank=True)
    SinCorrespondencia=models.IntegerField(blank=True, null=True)
    def __str__(self):
        return f'{self.fecha_transaccion} - {self.nombre}'

    class Meta:
        verbose_name = "Cliente_limpio"
        verbose_name_plural = "Cliente_Limpios"
class Proveedores(models.Model):
    contraparte = models.CharField(max_length=10, choices=Contraparte.TIPOS_CONTRAPARTE, default='Proveedor')
    fecha_transaccion = models.DateField()
    nit = models.CharField(max_length=20)
    nombre = models.CharField(max_length=255)
    ciiu = models.IntegerField()
    detalle=models.CharField(max_length=255)
    valor_transaccion = models.DecimalField(max_digits=30, decimal_places=2)
    pais = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=255)
    departamento = models.CharField(max_length=255)
    ano = models.IntegerField(blank=True, null=True)
    mes = models.IntegerField(blank=True, null=True)
    nombre_archivo = models.CharField(max_length=255, null=True, blank=True)
    tipo_de_persona = models.CharField(max_length=10)
    medio_de_pago = models.CharField(max_length=20)
    alarmas = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        return f'{self.fecha_transaccion} - {self.nombre}'

    class Meta:
        verbose_name = "P_limpio"
        verbose_name_plural = "P_Limpios"

class Generales (models.Model):
    departamento = models.CharField(max_length=255)
    municipio= models.CharField(max_length=255)
    divipola= models.CharField(max_length=255)
    categoria= models.CharField(max_length=255)
    valor_riesgo= models.IntegerField(blank=True, null=True)
    
    class Meta:
        verbose_name = "general"
        verbose_name_plural = "generales"


# class Usuaio():
#     id_empresa
#     nombre
#     correo
#     hash



# class empresa():
#     nombre
#     id
#     correo_oficial_cumplimiento
