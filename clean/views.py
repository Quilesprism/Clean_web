from django.shortcuts import render
import pandas as pd
from clean.models import Clientes, Proveedores, Generales
from . import limpieza
import os
from django.utils import timezone
from datetime import datetime
from django.contrib import messages 
from .guardarbd import guardarbd_proveedores, guardarCliente, cargar
from .alarmas import guardar_alarmas_y_promedio, guardar_alarmasP


def cargar_archivo(request):
    if request.method == 'POST':
        archivo = request.FILES.get('archivo')
        if not archivo:
            messages.error(request, 'No se proporcionó un archivo.')
        elif not archivo.name.endswith('.xlsx'):
            messages.error(request, 'Formato de archivo no válido. Debe ser un archivo XLSX.')
        else:
            tipo_contraparte = request.POST.get('tipo_contraparte')
            contraparte_handlers = {
                'cliente': procesar_cliente,
                'proveedor': procesar_proveedor,
                'empleado': procesar_empleado,
            }
            if tipo_contraparte in contraparte_handlers:
                return contraparte_handlers[tipo_contraparte](request)
            else:
                messages.error(request, 'Tipo de contraparte no válido')

    return render(request, 'cargar_archivo.html')

def procesar_cliente(request):
    columnas_requeridas = [
        "FECHA TRANSACCION",
        "No. DOCUMENTO DE IDENTIDAD",
        "NOMBRE",
        "CIIU",
        "NOMBRE DEL FUNCIONARIO RESPONSABLE DE LA VENTA",
        "VALOR DE LA TRANSACCION",
        "ID CENTRO COSTOS",
        "PAIS",
        "CIUDAD",
        "DEPARTAMENTO",
        "MEDIO PAGO",
        "TIPO PERSONA (natural/jurídica)",
        "CANAL DE DISTRIBUCION",
        "MEDIO DE VENTA"
    ]
    try:

        archivo = request.FILES.get('archivo')
        df = pd.read_excel(archivo)  
        columnas_archivo = df.columns.tolist()
        mismo_orden = columnas_requeridas == columnas_archivo
        todas_las_columnas_presentes = set(columnas_requeridas).issubset(columnas_archivo)
        if mismo_orden and todas_las_columnas_presentes:
                datos_generales = Generales.objects.all()
                data = list(datos_generales.values())
                df_gen = pd.DataFrame(data)
                print(df_gen.head())
                df_limpiado = limpieza.limpiar_dataframe(df, df_gen)
                df_final = limpieza.procesar_dataframes(df_limpiado, df_gen)
                print(df_final.head())
                nombre_alarmas = guardar_alarmas_y_promedio(df_final)  
                           
                fecha_subida = request.POST.get('fecha')

                if not fecha_subida:
                    messages.error(request, 'La fecha ingresada no es válida.')
                    return render(request, 'cargar_archivo.html')
                
                fecha_subida = datetime.strptime(fecha_subida, "%Y-%m-%d")
                ano_subida = fecha_subida.year
                mes_subida = fecha_subida.month

                if not Clientes.objects.filter(mes=mes_subida).exists():
                    fecha_actual = timezone.now()
                    nombre_archivo = f'Archivo_limpio_{fecha_actual.strftime("%Y%m%d%H%M%S")}.xlsx'
                    directorio_archivos = os.path.abspath('archivos_cargados')
                    
                    guardarCliente(df_final, ano_subida, mes_subida, nombre_archivo, nombre_alarmas)
                    
                    if not os.path.exists(directorio_archivos):
                        os.makedirs(directorio_archivos)
                    archivo_salida = os.path.join(directorio_archivos, nombre_archivo)
                    df_final.to_excel(archivo_salida, index=False)
                    messages.success(request, 'Archivo subido y limpiado correctamente')
                else:
                    messages.error(request, 'El archivo de mes o el año ingresado ya se encuentra en la base de datos')
            
        else:
            messages.error(request, 'El archivo no cumple con los requisitos de columnas y/o orden.')
            return render(request, 'cargar_archivo.html')
    except Exception as e:
                messages.error(request, f'Error al procesar el archivo: {str(e)}')

    return render(request, 'cargar_archivo.html')


def procesar_proveedor(request):
    columnas_requeridas = [
        "FECHA TRANSACCION",
        "No. DOCUMENTO DE IDENTIDAD",
        "NOMBRE",
        "CIIU",
        "DETALLE TRANSACCION",
        "VALOR DE LA TRANSACCION",
        "ID CENTRO COSTOS",
        "PAIS",
        "CIUDAD",
        "DEPARTAMENTO",
        "MEDIO PAGO",
        "TIPO PERSONA (natural/jurídica)",
    ]
    try:
        archivo = request.FILES.get('archivo')
        df = pd.read_excel(archivo)
        # resultado = cargar('C:/Users/quile/Downloads/GENERALES.xlsx')
        # if resultado is True:
        #   print("Datos cargados con éxito.")
        # else:
        #     print(f"Error al cargar datos: {resultado}")
        columnas_archivo = df.columns.tolist()
        mismo_orden = columnas_requeridas == columnas_archivo
        todas_las_columnas_presentes = set(columnas_requeridas).issubset(columnas_archivo)

        if mismo_orden and todas_las_columnas_presentes:
                    # El archivo cumple con los requisitos
                df_limpiado = limpieza.limpiar_Proveedor(df)
                fecha_subida = request.POST.get('fecha')
                nombre_alarmas = guardar_alarmasP(df_limpiado)                
                if not fecha_subida:
                    messages.error(request, 'La fecha ingresada no es válida.')
                    return render(request, 'cargar_archivo.html')
                
                fecha_subida = datetime.strptime(fecha_subida, "%Y-%m-%d")
                ano_subida = fecha_subida.year
                mes_subida = fecha_subida.month

                if not Proveedores.objects.filter(mes=mes_subida).exists():
                    fecha_actual = timezone.now()
                    nombre_archivo = f'Archivo_limpio_{fecha_actual.strftime("%Y%m%d%H%M%S")}.xlsx'
                    directorio_archivos = os.path.abspath('archivos_cargados')
                    
                    guardarbd_proveedores(df_limpiado, ano_subida, mes_subida, nombre_archivo, nombre_alarmas)
                    
                    if not os.path.exists(directorio_archivos):
                        os.makedirs(directorio_archivos)
                    archivo_salida = os.path.join(directorio_archivos, nombre_archivo)
                    df_limpiado.to_excel(archivo_salida, index=False)
                    messages.success(request, 'Archivo subido y limpiado correctamente')
                else:
                    messages.error(request, 'El archivo de mes o el año ingresado ya se encuentra en la base de datos')
            
        else:
            messages.error(request, 'El archivo no cumple con los requisitos de columnas y/o orden.')
            return render(request, 'cargar_archivo.html')
    except Exception as e:
                messages.error(request, f'Error al procesar el archivo: {str(e)}')

    return render(request, 'cargar_archivo.html')


def procesar_empleado(request):
    pass
