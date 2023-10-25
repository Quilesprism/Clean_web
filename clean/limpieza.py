import pandas as pd
import calendar
import re
from datetime import datetime
import unidecode

def limpiar_dataframe(df):
    try:
        def convertir_fecha(fecha_original):
            try:
                if pd.isnull(fecha_original):
                    return fecha_original  # retorna NaN si la fecha original es NaN
                str_fecha = str(fecha_original).strip()
                # Si la fecha termina en 2022 o 2023 y tiene 8 dígitos, intenta convertir en formato '%d%m%Y'
                if re.match(r'\d{8}', str_fecha) and (str_fecha.endswith('2022') or str_fecha.endswith('2023')):
                    return datetime.strptime(str_fecha, '%d%m%Y').replace(year=2023)
                else:
                    fecha_convertida= pd.to_datetime(str_fecha, errors='coerce', dayfirst=True)
                    return fecha_convertida.replace(year=2023) if not pd.isna(fecha_convertida) else fecha_original
            except Exception as e:
                return fecha_original

        df['FECHATRANSACCIÓN'] = df['FECHATRANSACCIÓN'].apply(convertir_fecha)

        # Asegurarse de que todos los valores sean o fechas válidas o NaT
        df['FECHATRANSACCIÓN'] = pd.to_datetime(df['FECHATRANSACCIÓN'], errors='coerce')

        # Si hay al menos una fecha no nula en la columna, proceder con el reemplazo de las fechas nulas
        if df['FECHATRANSACCIÓN'].dropna().shape[0] > 0:
            # Obtener el año y el mes más frecuentes entre las fechas válidas
            fecha_mas_frecuente = df['FECHATRANSACCIÓN'].dropna().dt.to_period("M").mode()[0].to_timestamp()
            ano = fecha_mas_frecuente.year
            mes = fecha_mas_frecuente.month

            # Calcular el último día del mes
            ultimo_dia = calendar.monthrange(ano, mes)[1]

            # Crear una fecha con el último día del mes y año más frecuentes
            fecha_ultimo_dia = pd.Timestamp(year=ano, month=mes, day=ultimo_dia)

            # Reemplazar las fechas nulas con la fecha calculada
            df['FECHATRANSACCIÓN'].fillna(fecha_ultimo_dia, inplace=True)

        df['FECHATRANSACCIÓN'] = pd.to_datetime(df['FECHATRANSACCIÓN'], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')

        def limpiar_nit(nit):
            nit = str(nit)
            nit = re.sub('[^0-9-]', '', nit)  # Elimina caracteres no deseados
            partes = nit.split('-')
            if len(partes) > 1 and len(partes[1]) <= 3:  # Si hay un guión seguido por máximo 3 dígitos
                nit = partes[0]  # Conserva solo la parte antes del guión
            if nit =='':
                return '9999'
            return nit

        df['Nit'] = df['Nit'].apply(limpiar_nit)

        def limpiar_nombre(nombre):
            nombre = unidecode.unidecode(nombre)  # Eliminar acentos
            nombre = re.sub('[^A-Z0-9 ]+', '', nombre.upper())  # Eliminar caracteres especiales y convertir a mayúsculas
            nombre = re.sub(' +', ' ', nombre).strip()  # Reemplazar espacios múltiples por uno solo y eliminar espacios al principio y al final
            return nombre

        df['Nombre'] = df['Nombre'].apply(limpiar_nombre)

        df['CIIU'] = pd.to_numeric(df['CIIU'], errors='coerce')
        df['CIIU'].fillna(9999, inplace=True)
        df['CIIU'] = df['CIIU'].astype(int)

        def obtener_mayoritario(grupo):
            moda = grupo.mode()
            if moda.empty or moda.size > 1:
                return 9999
            return moda.iloc[0]

        # Agrupa por 'Nit' y calcula el valor mayoritario de 'CIIU' para cada grupo
        df['CIIU'] = df.groupby('Nit')['CIIU'].transform(obtener_mayoritario)

        df['ValordelaTransacción'] = df['ValordelaTransacción'].replace('', 0)

        def ajustar_ciudad_pais_fila(fila):
            # Limpiar caracteres especiales de todas las columnas relevantes
            fila['PAIS'] = re.sub(r'[^A-Za-z0-9-& ]+', '', fila['PAIS'])
            fila['CIUDAD'] = re.sub(r'[^A-Za-z0-9-& ]+', '', fila['CIUDAD'])
            fila['DEPARTAMENTO'] = re.sub(r'[^A-Za-z0-9-& ]+', '', fila['DEPARTAMENTO'])

            # Si IDPAIS es distinto a COLOMBIA, ajustar IDCIUDAD y IDDEPTO
            if fila['PAIS'].upper() != 'COLOMBIA':
                fila['CIUDAD'] = fila['CIUDAD']
                fila['DEPARTAMENTO'] = 'EXTRANJERO'
            return fila

        # Función para limpiar caracteres especiales
        def limpiar_caracteres(cadena):
            if pd.isna(cadena):  # Si el valor es NaN, simplemente retornar como está
                return cadena
            cadena_limpia = re.sub(r'[^a-zA-Z0-9ñÑáéíóúÁÉÍÓÚ\s]', '', cadena)
            return cadena_limpia.strip()

        return df
    except Exception as e:
        enviar_correo_electronico("Error al limpiar el DataFrame: " + str(e))

from django.core.mail import send_mail

def enviar_correo_electronico(mensaje):
    subject = 'Error en la aplicación'  
    message = mensaje 
    from_email = 'quilesxasterin8@gmail.com'  
    recipient_list = ['quilesxasterin8@gmail.com']  

    send_mail(subject, message, from_email, recipient_list)
