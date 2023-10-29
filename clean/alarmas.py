from django.utils import timezone
import os

def guardar_alarmas_y_promedio(df):
    carpeta = 'alarmas'
    columnas_deseadas = ['No. DOCUMENTO DE IDENTIDAD', 'NOMBRE', 'VALOR DE LA TRANSACCION', 'ALARMAS']

    df_filtrado = df[df['ALARMAS'].isin(['INUSUAL', 'SOSPECHOSA'])]

    df_filtrado = df_filtrado[columnas_deseadas]
    
    fecha_actual = timezone.now()
    nombre_archivo = f'Alarmas_{fecha_actual.strftime("%Y%m%d%H%M%S")}.xlsx'
    
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    
    ruta_completa = os.path.join(carpeta, nombre_archivo)
    
    df_filtrado.to_excel(ruta_completa, index=False)
    
    return nombre_archivo




