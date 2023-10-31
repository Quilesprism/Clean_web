from django.utils import timezone
import os

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
    columnas_deseadas = ['No. DOCUMENTO DE IDENTIDAD', 'NOMBRE', 'VALOR DE LA TRANSACCION', 'ALARMAS']
    df_filtrado = df[df['ALARMAS'].isin(['INUSUAL', 'SOSPECHOSA'])]
    df_filtrado = df_filtrado[columnas_deseadas]
    print(df_filtrado.head())
    fecha_actual = timezone.now()
    nombre_archivo = f'Alarmas_{fecha_actual.strftime("%Y%m%d%H%M%S")}.xlsx'
    if not os.path.exists(carpeta):
        os.makedirs(carpeta) 
    ruta_completa = os.path.join(carpeta, nombre_archivo)
    df_filtrado.to_excel(ruta_completa, index=False)
    return nombre_archivo




