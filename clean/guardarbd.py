from .models import Clientes, Generales, Proveedores

from django.db import transaction
import pandas as pd

@transaction.atomic
def guardarCliente(df_limpiado, ano_subida, mes_subida, nombre_archivo, nombre_alarmas):
    clientes = []
    for index, row in df_limpiado.iterrows():
        cliente_data = {
            'fecha_transaccion': row['FECHA TRANSACCION'],
            'nit': row['No. DOCUMENTO DE IDENTIDAD'],
            'nombre': row['NOMBRE'],
            'ciiu': row['CIIU'],
            'valor_transaccion': row['VALOR DE LA TRANSACCION'],
            'pais': row['PAIS'],
            'ciudad': row['CIUDAD'],
            'departamento': row['DEPARTAMENTO'],
            'funcionario': row['NOMBRE DEL FUNCIONARIO RESPONSABLE DE LA VENTA'],
            'tipo_de_persona': row['TIPO PERSONA'],
            'medio_de_pago': row['MEDIO PAGO'],
            'canal_de_distribucion': row['CANAL DE DISTRIBUCION'],
            'medio_de_venta': row['MEDIO DE VENTA'],
            'ano': ano_subida,
            'mes': mes_subida,
            'nombre_archivo': nombre_archivo,
            'alarmas': nombre_alarmas,
            'Concatenado': row['Concatenado'],
            'SinCorr_Ciudad': row['SinCorr_Ciudad'],
            'SinCorrespondencia': row['SinCorrespondencia'],
            'contraparte': 'Cliente'
        }
        cliente = Clientes(
            **cliente_data
        )
        clientes.append(cliente)

    Clientes.objects.bulk_create(clientes)


@transaction.atomic
def guardarbd_proveedores(df_limpiado, ano_subida, mes_subida, nombre_archivo, nombre_alarmas):
    proveedores=[]
    for index, row in df_limpiado.iterrows():
        proveedor = Proveedores(
            fecha_transaccion=row['FECHA TRANSACCION'],
            nit=row['No. DOCUMENTO DE IDENTIDAD'],
            nombre=row['NOMBRE'],
            ciiu=row['CIIU'],
            detalle=row['DETALLE TRANSACCION'],
            valor_transaccion=row['VALOR DE LA TRANSACCION'],
            pais=row['PAIS'],
            ciudad=row['CIUDAD'],
            departamento=row['DEPARTAMENTO'],
            ano=ano_subida,
            mes=mes_subida,
            nombre_archivo=nombre_archivo,
            tipo_de_persona=row['TIPO PERSONA'],
            medio_de_pago=row['MEDIO PAGO'],
            alarmas=nombre_alarmas,
            
            contraparte= 'Proveedor'
        )
        proveedores.append(proveedor)
    Proveedores.objects.bulk_create(proveedores)

@transaction.atomic
def cargar(file_path):
    try:

        df = pd.read_excel(file_path)
        generales=[]
        for index, row in df.iterrows():
              instancia_modelo = Generales(
                departamento=row['Departamento'],
                 municipio=row['Municipio'],
                 divipola=row['Divipola'],
                 categoria=row['Categoria'],
                 valor_riesgo=row['VALOR-RIESGO']
            )
              generales.append(instancia_modelo) 
        
        Generales.objects.bulk_create(generales)
        return True
    except Exception as e:
        return str(e)