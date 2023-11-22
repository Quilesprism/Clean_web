from .models import CIIU, Clientes, Jurisdiccion, Proveedores

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
def cargar_jurisdiccion(ruta_excel):
    try:
        xls = pd.ExcelFile(ruta_excel)
        jurisdicciones = []

        for hoja_nombre in xls.sheet_names:
            if hoja_nombre == 'JURISDICCIÓN':
                df_limpiado = xls.parse(hoja_nombre)

                for index, row in df_limpiado.iterrows():
                    jurisdiccion = Jurisdiccion(
                        departamento=row['Departamento'],
                        municipio=row['Municipio'],
                        divipola=row['Divipola'],
                        categoria=row['Categoria'],
                        valor_riesgo=row['VALOR-RIESGO'],
                     
                    )
                    jurisdicciones.append(jurisdiccion)

                Jurisdiccion.objects.bulk_create(jurisdicciones)

        return True
    except Exception as e:
        print(f"Error al cargar datos de Jurisdiccion: {e}")
        return False

@transaction.atomic
def cargar_ciiu(ruta_excel):
    try:
        xls = pd.ExcelFile(ruta_excel)
        ciius = []

        for hoja_nombre in xls.sheet_names:
            if hoja_nombre == 'CIIU':
                df_limpiado = xls.parse(hoja_nombre)

                for index, row in df_limpiado.iterrows():
                    ciiu = CIIU(
                        cod_ciiu=row['Cod_Ciiu'],
                        seccion=row['Seccion'],
                        division=row['Division'],
                        grupo=row['Grupo'],
                        descripcion=row['Descripcion'],
                        valor_riesgo=row['VALOR- RIESGO'],
                        
                    )
                    ciius.append(ciiu)

                CIIU.objects.bulk_create(ciius)

        return True
    except Exception as e:
        print(f"Error al cargar datos de CIIU: {e}")
        return False