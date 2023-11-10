from django.utils import timezone
import os
from django.core.mail import EmailMessage
from matplotlib import pyplot as plt

def enviar_correo_electronico(mensaje, archivo_adjunto):
    subject = 'Archivo de Alarmas'
    from_email = 'quilesxasterin8@gmail.com'
    recipient_list = ['quilesxasterin8@gmail.com']
    email = EmailMessage(subject, mensaje, from_email, recipient_list)
    with open(archivo_adjunto, 'rb') as file:
        email.attach(os.path.basename(archivo_adjunto), file.read(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    email.send()
# def enviar_correo_electronico_con_imagen(mensaje, imagen_adjunta):
#     subject = 'Archivo de Alarmas'
#     from_email = 'quilesxasterin8@gmail.com'
#     recipient_list = ['quilesxasterin8@gmail.com']
#     email = EmailMessage(subject, mensaje, from_email, recipient_list)
#     with open(imagen_adjunta, 'rb') as file:
#         email.attach_file(imagen_adjunta, mimetype='image/png')  # Ajusta el mimetype según el tipo de imagen
#     email.send()

def guardar_alarmas_y_promedio(df):
    # Calcular el promedio del VALOR DE LA TRANSACCION por No. DOCUMENTO DE IDENTIDAD
    df['PROMEDIO'] = df.groupby('No. DOCUMENTO DE IDENTIDAD')['VALOR DE LA TRANSACCION'].transform('mean')
    # Crear la columna ALARMAS con valores por defecto NORMAL
    df['ALARMAS'] = 'USUAL'
    #cambiar a sospechoso si la transacción es mayor a 10 millones
    df.loc[df['VALOR DE LA TRANSACCION'] > 10000000, 'ALARMAS'] = 'SOSPECHOSA_NORMAL'
    # Cambiar a INUSUAL si alguna transacción es al menos cinco veces mayor al promedio
    df.loc[df['VALOR DE LA TRANSACCION'] >= 5 * df['PROMEDIO'], 'ALARMAS'] = 'INUSUAL'
    # Cambiar a SOSPECHOSA si además la transacción se realizó con MEDIO PAGO EFECTIVO
    df.loc[(df['ALARMAS'] == 'INUSUAL') & (df['MEDIO PAGO'] == 'EFECTIVO'), 'ALARMAS'] = 'SOSPECHOSA_EFECTIVO'    

    
    carpeta = 'alarmas'
    columnas_deseadas = ['FECHA TRANSACCION', 'No. DOCUMENTO DE IDENTIDAD', 'NOMBRE', 'VALOR DE LA TRANSACCION', 'PROMEDIO', 'MEDIO PAGO', 'TIPO PERSONA (natural/jurídica)', 'CANAL DE DISTRIBUCION', 'ALARMAS']
    df_filtrado = df[df['ALARMAS'].isin(['INUSUAL', 'SOSPECHOSA_NORMAL', 'SOSPECHOSA_EFECTIVO'])]
    df_filtrado = df_filtrado[columnas_deseadas]
    counts = df['ALARMAS'].value_counts()
    labels = counts.index
    plt.pie(counts, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title('Distribución de Alarmas')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Guardar la gráfica en una imagen
    carpeta_graficas = 'graficas'
    if not os.path.exists(carpeta_graficas):
        os.makedirs(carpeta_graficas)

    ruta_grafica = os.path.join(carpeta_graficas, 'Distribucion_Alarmas.png')
    plt.savefig(ruta_grafica)
    plt.close()

    subject = 'Archivo de Alarmas'
    mensaje = 'Adjunto encontrarás el gráfico de las alarmas.'

    from_email = 'quilesxasterin8@gmail.com'
    recipient_list = ['quilesxasterin8@gmail.com']
    email = EmailMessage(subject, mensaje, from_email, recipient_list)


    with open(ruta_grafica, 'rb') as file:
        email.attach('Distribucion_Alarmas.png', file.read(), 'image/png')

    email.send()
    fecha_actual = timezone.now()
    nombre_archivo = f'Alarmas_{fecha_actual.strftime("%Y%m%d%H%M%S")}.xlsx'
    if not os.path.exists(carpeta):
        os.makedirs(carpeta) 
    ruta_completa = os.path.join(carpeta, nombre_archivo)
    df_filtrado.to_excel(ruta_completa, index=False)
    mensaje='Archivo de alarmas'
    enviar_correo_electronico(mensaje, ruta_completa)
    return nombre_archivo

def guardar_alarmasP(df):
    df['PROMEDIO'] = df.groupby('FECHA TRANSACCION', 'No. DOCUMENTO DE IDENTIDAD')['VALOR DE LA TRANSACCION'].transform('mean')
    df['ALARMAS'] = 'USUAL'
    df.loc[df['VALOR DE LA TRANSACCION'] >= 5 * df['PROMEDIO'], 'ALARMAS'] = 'INUSUAL'
    df.loc[(df['ALARMAS'] == 'INUSUAL') & (df['MEDIO PAGO'] == 'EFECTIVO'), 'ALARMAS'] = 'SOSPECHOSA'    
    df.loc[df['VALOR DE LA TRANSACCION'] > 10000000, 'ALARMAS'] = 'SOSPECHOSA'
    carpeta = 'alarmas'
    columnas_deseadas = ['FECHA TRANSACCION', 'No. DOCUMENTO DE IDENTIDAD', 'NOMBRE', 'VALOR DE LA TRANSACCION', 'PROMEDIO', 'MEDIO PAGO', 'TIPO PERSONA (natural/jurídica)', 'ALARMAS']
    df_filtrado = df[df['ALARMAS'].isin(['INUSUAL', 'SOSPECHOSA'])]
    df_filtrado = df_filtrado[columnas_deseadas]
    fecha_actual = timezone.now()
    nombre_archivo = f'Alarmas_{fecha_actual.strftime("%Y%m%d%H%M%S")}.xlsx'
    if not os.path.exists(carpeta):
        os.makedirs(carpeta) 
    ruta_completa = os.path.join(carpeta, nombre_archivo)
    df_filtrado.to_excel(ruta_completa, index=False)
    mensaje='Archivo de alarmas'
    enviar_correo_electronico(mensaje, ruta_completa)
    return nombre_archivo


