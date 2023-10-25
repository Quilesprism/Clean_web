from django.db import models

class DatosLimpios(models.Model):
    fecha_transaccion = models.DateField()
    nit = models.CharField(max_length=20)
    nombre = models.CharField(max_length=255)
    ciiu = models.IntegerField()
    valor_transaccion = models.DecimalField(max_digits=10, decimal_places=2)
    pais = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=255)
    departamento = models.CharField(max_length=255)
    ano = models.IntegerField(blank=True, null=True)  
    mes = models.IntegerField(blank=True, null=True) 
    nombre_archivo = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        return f'{self.fecha_transaccion} - {self.nombre}'

    class Meta:
        verbose_name = "Dato_limpio"
        verbose_name_plural = "Datos_Limpios"
