import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import os
import base64
import urllib.parse
from django.core.mail import EmailMessage
from django.utils import timezone

def enviar_correo_electronico(mensaje, archivo_adjunto):
    subject = 'Archivo de Alarmas'
    from_email = 'quilesxasterin8@gmail.com'
    recipient_list = ['quilesxasterin8@gmail.com']
    email = EmailMessage(subject, mensaje, from_email, recipient_list)
    with open(archivo_adjunto, 'rb') as file:
        email.attach(os.path.basename(archivo_adjunto), file.read(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    email.send()

def guardar_alarmas_y_promedio(df):
    # Calcular el promedio del VALOR DE LA TRANSACCION por No. DOCUMENTO DE IDENTIDAD
    df['PROMEDIO'] = df.groupby('No. DOCUMENTO DE IDENTIDAD')['VALOR DE LA TRANSACCION'].transform('mean')
    # Crear la columna ALARMAS con valores por defecto NORMAL
    df['ALARMAS'] = 'USUAL'
    # Cambiar a INUSUAL si alguna transacción es al menos cinco veces mayor al promedio
    df.loc[df['VALOR DE LA TRANSACCION'] >= 5 * df['PROMEDIO'], 'ALARMAS'] = 'INUSUAL'
    # Cambiar a SOSPECHOSA si además la transacción se realizó con MEDIO PAGO EFECTIVO
    df.loc[(df['ALARMAS'] == 'INUSUAL') & (df['MEDIO PAGO'] == 'EFECTIVO'), 'ALARMAS'] = 'SOSPECHOSA'    
    #cambiar a sospechoso si la transacción es mayor a 10 millones
    df.loc[df['VALOR DE LA TRANSACCION'] > 10000000, 'ALARMAS'] = 'SOSPECHOSA'
    carpeta = 'alarmas'
    columnas_deseadas = ['No. DOCUMENTO DE IDENTIDAD', 'NOMBRE', 'VALOR DE LA TRANSACCION', 'MEDIO PAGO', 'TIPO PERSONA (natural/jurídica)', 'CANAL DE DISTRIBUCION', 'ALARMAS']
    df_filtrado = df[df['ALARMAS'].isin(['INUSUAL', 'SOSPECHOSA'])]
    df_filtrado = df_filtrado[columnas_deseadas]
    counts = df['ALARMAS'].value_counts()
    labels = counts.index
    plt.pie(counts, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title('Distribución de Alarmas')
    plt.axis('equal') 
    carpeta = 'alarmas'
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    carpeta_graficas = 'graficas'
    if not os.path.exists(carpeta_graficas):
        os.makedirs(carpeta_graficas)
    ruta_grafica = os.path.join(carpeta_graficas, 'Distribucion_Alarmas.png')
    plt.savefig(ruta_grafica)
    plt.close()
    subject = 'Archivo de Alarmas'
    mensaje = 'Adjunto encontrarás el gráfico y el archivo de las alarmas.'
    from_email = 'notificaciones@riesgos365.com'
    recipient_list = ['contacto@omenlaceglobal.co']
    # from_email = 'quilesxasterin8@gmail.com'
    # recipient_list = ['quilesxasterin8@gmail.com']
    email = EmailMessage(subject, mensaje, from_email, recipient_list)
    with open(ruta_grafica, 'rb') as file:
        email.attach('Distribucion_Alarmas.png', file.read(), 'image/png')
    fecha_actual = timezone.now()
    nombre_archivo = f'Alarmas_{fecha_actual.strftime("%Y%m%d%H%M%S")}.xlsx'
    ruta_completa = os.path.join(carpeta, nombre_archivo)
    df_filtrado.to_excel(ruta_completa, index=False)
    with open(ruta_completa, 'rb') as file:
        email.attach(nombre_archivo, file.read(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    email.send()
    return nombre_archivo


def guardar_alarmasP(df):
    df['PROMEDIO'] = df.groupby('No. DOCUMENTO DE IDENTIDAD')['VALOR DE LA TRANSACCION'].transform('mean')
    df['ALARMAS'] = 'USUAL'
    df.loc[df['VALOR DE LA TRANSACCION'] >= 5 * df['PROMEDIO'], 'ALARMAS'] = 'INUSUAL'
    df.loc[(df['ALARMAS'] == 'INUSUAL') & (df['MEDIO PAGO'] == 'EFECTIVO'), 'ALARMAS'] = 'SOSPECHOSA'
    df.loc[df['VALOR DE LA TRANSACCION'] > 10000000, 'ALARMAS'] = 'SOSPECHOSA'
    columnas_deseadas = ['No. DOCUMENTO DE IDENTIDAD', 'NOMBRE', 'VALOR DE LA TRANSACCION', 'MEDIO PAGO', 'TIPO PERSONA (natural/jurídica)', 'ALARMAS']
    df_filtrado = df[df['ALARMAS'].isin(['INUSUAL', 'SOSPECHOSA'])]
    df_filtrado = df_filtrado[columnas_deseadas]
    counts = df_filtrado['ALARMAS'].value_counts()
    labels = counts.index
    plt.pie(counts, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title('Distribución de Alarmas')
    plt.axis('equal')

    # Guardar el gráfico en un buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Codificar el gráfico en base64
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    context = {'imgdata': uri}

    # Adjuntar el gráfico y el archivo al correo
    subject = 'Archivo de Alarmas'
    mensaje = 'Adjunto encontrarás el gráfico y el archivo de las alarmas.'
    from_email = 'notificaciones@riesgos365.com'
    recipient_list = ['contacto@omenlaceglobal.co']
    email = EmailMessage(subject, mensaje, from_email, recipient_list)

    # Adjuntar el gráfico al correo
    email.attach('Distribucion_Alarmas.png', buf.getvalue(), 'image/png')

    # Guardar el archivo de alarmas en la carpeta de archivos
    fecha_actual = timezone.now()
    carpeta = 'alarmas'
    nombre_archivo = f'Alarmas_{fecha_actual.strftime("%Y%m%d%H%M%S")}.xlsx'
    ruta_completa = os.path.join(carpeta, nombre_archivo)
    df_filtrado.to_excel(ruta_completa, index=False)

    # Adjuntar el archivo al correo
    with open(ruta_completa, 'rb') as file:
        email.attach(nombre_archivo, file.read(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    # Enviar el correo electrónico
    email.send()

    # Cerrar el gráfico
    plt.close()

    return nombre_archivo



