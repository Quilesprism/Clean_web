import calendar
import locale
import os
from django.db.models import Count
from django.shortcuts import redirect, render
from clean.models import Clientes, Proveedores
from django.contrib import messages 

def limpiados(request):
    return render(request, 'limpiados.html')

def obtener_nombre_mes(numero_mes):
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    nombre_mes = calendar.month_name[numero_mes]
    locale.setlocale(locale.LC_TIME, '')
    return nombre_mes

def mostrar_todos_los_meses(request):
    clientes = Clientes.objects.values('ano', 'mes').annotate(cantidad_registros=Count('mes'))
    proveedores = Proveedores.objects.values('ano', 'mes').annotate(cantidad_registros=Count('mes'))

    meses_y_nombres = []

    for mes_registro in clientes:
        objetos = Clientes.objects.filter(ano=mes_registro['ano'], mes=mes_registro['mes'])
        if objetos.exists():
            primer_objeto = objetos.first()
            nombre_archivo = primer_objeto.nombre_archivo
            objeto_alarmas = objetos.last()
            nombre_alarmas = objeto_alarmas.alarmas
        else:
            nombre_archivo = None

        meses_y_nombres.append({
            'ano': mes_registro['ano'],
            'mes': mes_registro['mes'],
            'nombre_mes': obtener_nombre_mes(mes_registro['mes']),
            'cantidad_registros': mes_registro['cantidad_registros'],
            'nombre_archivo': nombre_archivo,
            'tipo_contraparte': 'Clientes',
            'nombre_alarmas': nombre_alarmas,
        })

    for mes_registro in proveedores:
        objetos = Proveedores.objects.filter(ano=mes_registro['ano'], mes=mes_registro['mes'])
        if objetos.exists():
            primer_objeto = objetos.first()
            nombre_archivo = primer_objeto.nombre_archivo
            objeto_alarmas = objetos.last()
            nombre_alarmas = objeto_alarmas.alarmas
        else:
            nombre_archivo = None

        meses_y_nombres.append({
            'ano': mes_registro['ano'],
            'mes': mes_registro['mes'],
            'nombre_mes': obtener_nombre_mes(mes_registro['mes']),
            'cantidad_registros': mes_registro['cantidad_registros'],
            'nombre_archivo': nombre_archivo,
            'tipo_contraparte': 'Proveedores',
            'nombre_alarmas': nombre_alarmas,
        })

    meses_y_nombres.sort(key=lambda x: (-x['mes']))

    return render(request, 'tabla_mes.html', {'meses_y_nombres': meses_y_nombres})


def mostrar_todos_los_anios(request):
    clientes = Clientes.objects.values('ano').annotate(cantidad_registros=Count('ano'))
    proveedores = Proveedores.objects.values('ano').annotate(cantidad_registros=Count('ano'))

    años_y_registros = []

    for año_registro in clientes:
        contraparte = 'Clientes'
        años_y_registros.append({
            'ano': año_registro['ano'],
            'cantidad_registros': año_registro['cantidad_registros'],
            'tipo_contraparte': contraparte,
        })

    for año_registro in proveedores:
        contraparte = 'Proveedores'
        años_y_registros.append({
            'ano': año_registro['ano'],
            'cantidad_registros': año_registro['cantidad_registros'],
            'tipo_contraparte': contraparte,
        })

    return render(request, 'tabla_año.html', {'años_y_registros': años_y_registros})



from django.http import FileResponse
from django.core.exceptions import ObjectDoesNotExist

def descargar_archivo(request, ano, mes, contraparte):
    try:
        if contraparte == 'Clientes':
            datos_limpios = Clientes.objects.filter(ano=ano, mes=mes).first()
        elif contraparte == 'Proveedores':
            datos_limpios = Proveedores.objects.filter(ano=ano, mes=mes).first()
        else:
            messages.error(request, 'Tipo de contraparte no válido.')
            return redirect('mostrar_todos_los_meses')

        nombre_archivo = datos_limpios.nombre_archivo if datos_limpios else None

        if nombre_archivo:
            directorio_archivos = os.path.abspath('archivos_cargados/')
            archivo_path = os.path.join(directorio_archivos, nombre_archivo)

            # Configurar la respuesta para la descarga
            response = FileResponse(open(archivo_path, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
            return response
        else:
            # Manejo de errores si el archivo no está disponible para descargar
            messages.error(request, 'El archivo no está disponible para descargar.')
            return redirect('mostrar_todos_los_meses')
    except ObjectDoesNotExist:
        # Manejo de errores si no se encuentra ningún objeto
        messages.error(request, 'No se encontraron datos para el año y mes especificados.')
        return redirect('mostrar_todos_los_meses')

def descargar_alarma(request, ano, mes, contraparte):
    try:
        if contraparte == 'Clientes':
            datos_limpios = Clientes.objects.filter(ano=ano, mes=mes).first()
        elif contraparte == 'Proveedores':
            datos_limpios = Proveedores.objects.filter(ano=ano, mes=mes).first()
        else:
            messages.error(request, 'Tipo de contraparte no válido.')
            return redirect('mostrar_todos_los_meses')

        nombre_alarma = datos_limpios.alarmas if datos_limpios else None

        if nombre_alarma:
            directorio_archivos = os.path.abspath('alarmas/')
            archivo_path = os.path.join(directorio_archivos, nombre_alarma)

            # Configurar la respuesta para la descarga
            response = FileResponse(open(archivo_path, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{nombre_alarma}"'
            return response
        else:
            # Manejo de errores si el archivo no está disponible para descargar
            messages.error(request, 'El archivo no está disponible para descargar.')
            return redirect('mostrar_todos_los_meses')
    except ObjectDoesNotExist:
        # Manejo de errores si no se encuentra ningún objeto
        messages.error(request, 'No se encontraron datos para el año y mes especificados.')
        return redirect('mostrar_todos_los_meses')
