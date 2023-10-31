
from django.http import JsonResponse
from django.shortcuts import render
import pandas as pd
from clean.models import Clientes
from . import limpieza
import os
from django.utils import timezone
from datetime import datetime
from django.contrib import messages 
from .guardarbd import guardarbd_proveedores, guardarCliente
from .alarmas import guardar_alarmas_y_promedio

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
                request.session['tipo_contraparte'] = tipo_contraparte
                return contraparte_handlers[tipo_contraparte](request)
            else:
                messages.error(request, 'Tipo de contraparte no válido')

    return render(request, 'cargar_archivo.html')

def procesar_cliente(request):
    try:
        archivo = request.FILES.get('archivo')
        
        df = pd.read_excel(archivo)
        df_limpiado = limpieza.limpiar_dataframe(df)
        print(df.head())
        fecha_subida = request.POST.get('fecha')
        nombre_alarmas = guardar_alarmas_y_promedio(df_limpiado)
        
        
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
            
            guardarCliente(df_limpiado, ano_subida, mes_subida, nombre_archivo, nombre_alarmas)
            
            if not os.path.exists(directorio_archivos):
                os.makedirs(directorio_archivos)
            archivo_salida = os.path.join(directorio_archivos, nombre_archivo)
            df_limpiado.to_excel(archivo_salida, index=False)
            messages.success(request, 'Archivo subido y limpiado correctamente')
        else:
            messages.error(request, 'El archivo de mes o el año ingresado ya se encuentra en la base de datos')
    except Exception as e:
        messages.error(request, f'Error al procesar el archivo: {str(e)}')
    
    return render(request, 'cargar_archivo.html')


def procesar_proveedor(request):
    pass

def procesar_empleado(request):
    pass
