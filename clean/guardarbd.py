from .models import Clientes, Proveedores

from django.db import transaction
import pandas as pd

@transaction.atomic
def guardarCliente(df_limpiado, ano_subida, mes_subida, nombre_archivo, nombre_alarmas):
    clientes = []
    for index, row in df_limpiado.iterrows():
        cliente = Clientes(
            fecha_transaccion=row['FECHA TRANSACCION'],
            nit=row['No. DOCUMENTO DE IDENTIDAD'],
            nombre=row['NOMBRE'],
            ciiu=row['CIIU'],
            valor_transaccion=row['VALOR DE LA TRANSACCION'],
            pais=row['PAIS'],
            ciudad=row['CIUDAD'],
            departamento=row['DEPARTAMENTO'],
            funcionario=row['NOMBRE DEL FUNCIONARIO RESPONSABLE DE LA VENTA'],
            tipo_de_persona=row['TIPO PERSONA'],
            medio_de_pago=row['MEDIO PAGO'],
            canal_de_distribucion=row['CANAL DE DISTRIBUCION'],
            medio_de_venta=row['MEDIO DE VENTA'],
            ano=ano_subida,
            mes=mes_subida,
            nombre_archivo=nombre_archivo,
            alarmas=nombre_alarmas
        )
        clientes.append(cliente)

    Clientes.objects.bulk_create(clientes)


def guardarbd_proveedores(df_limpiado, ano_subida, mes_subida, nombre_archivo):
    for index, row in df_limpiado.iterrows():
        proveedor = Proveedores(
            fecha_transaccion=row['FECHA TRANSACCION'],
            nit=row['No. DOCUMENTO DE IDENTIDAD'],
            nombre=row['NOMBRE'],
            ciiu=row['CIIU'],
            valor_transaccion=row['VALOR DE LA TRANSACCION'],
            pais=row['PAIS'],
            ciudad=row['CIUDAD'],
            departamento=row['DEPARTAMENTO'],
            ano=ano_subida,
            mes=mes_subida,
            nombre_archivo=nombre_archivo,
            funcionario=row['NOMBRE DEL FUNCIONARIO RESPONSABLE DE LA VENTA'],
            tipo_de_persona=row['TIPO PERSONA'],
            medio_de_pago=row['MEDIO PAGO']
        )
        proveedor.save()