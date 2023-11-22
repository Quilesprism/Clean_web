
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import os
import base64
import urllib.parse
from django.core.mail import EmailMessage
from django.utils import timezone

def segmentacion_c(df_actual, df_gen_c, df_gen_j):
    df_actual['Resultado_CIIU'] = df_actual['CIIU'].map(df_gen_c.set_index('cod_ciiu')['valor_riesgo']) * 0.1
    df_actual['Resultado_CIIU'].fillna(df_actual[-df_actual['Resultado_CIIU'].isna()]['Resultado_CIIU'].mean(), inplace=True)
    print(df_actual['Resultado_CIIU'])

    df_actual['Concatenacion_Dep_Ciudad'] = df_actual['DEPARTAMENTO'] + df_actual['CIUDAD']
    df_gen_j['Concatenacion'] = df_gen_j['departamento'] + df_gen_j['municipio']
    df_gene_sin_duplicados = df_gen_j.groupby('Concatenacion')['valor_riesgo'].mean().reset_index()

    df_actual['Resultado_Jurisdiccion'] = df_actual['Concatenacion_Dep_Ciudad'].map(df_gene_sin_duplicados.set_index('Concatenacion')['valor_riesgo']) * 0.15
    df_actual['Resultado_Jurisdiccion'].fillna(0, inplace=True)
    print(df_actual['Resultado_Jurisdiccion'])
    
    df_actual['Resultado_Mediopago'] = df_actual['MEDIO PAGO'].apply(lambda x: 5 if x == 'EFECTIVO' else 1)* 0.15
    print(df_actual['Resultado_Mediopago'])
    
    df_actual['Resultado_persona'] = df_actual['TIPO PERSONA (natural/jurídica)'].apply(lambda x: 5 if x == 'NATURAL' else 1)* 0.45
    print(df_actual['Resultado_persona'])
    
    df_actual['Resultado_pr'] = df_actual.groupby('No. DOCUMENTO DE IDENTIDAD')['VALOR DE LA TRANSACCION'].transform('mean')
    df_actual['Resultado_pr'].fillna(0, inplace=True) 
    print(df_actual['Resultado_pr'])
    
    promedio_por_grupo = df_actual.groupby('No. DOCUMENTO DE IDENTIDAD')['VALOR DE LA TRANSACCION'].transform('mean')
    primer_dato_por_grupo = df_actual.groupby('No. DOCUMENTO DE IDENTIDAD')['VALOR DE LA TRANSACCION'].transform('first')
    
    df_actual['Resultado_promedio'] = primer_dato_por_grupo / promedio_por_grupo.where(df_actual.groupby('No. DOCUMENTO DE IDENTIDAD')['VALOR DE LA TRANSACCION'].transform('count') > 1)
    df_actual['Resultado_promedio'].fillna(0, inplace=True) 
    df_actual['Resultado_promedio'] = pd.to_numeric(df_actual['Resultado_promedio'])
    print(df_actual['Resultado_promedio'])
    
    df_actual['Resultado'] = pd.cut(df_actual['Resultado_promedio'], bins=[0, 10, 15, 20, 30, float('inf')], labels=[1, 2, 3, 4, 5], right=False).astype(int) * 0.45
    print(df_actual['Resultado'])

    columnas_deseadas = ['No. DOCUMENTO DE IDENTIDAD', 
                         'NOMBRE', 'VALOR DE LA TRANSACCION', 
                         'MEDIO PAGO', 
                         'TIPO PERSONA (natural/jurídica)', 
                         'Resultado_CIIU', 
                         'Resultado_Jurisdiccion',
                         'Resultado_Mediopago', 
                         'Resultado_persona',
                         'Resultado'
                         ]
    df_filtrado = df_actual[columnas_deseadas]
    columnas_contar = ['Resultado_CIIU', 'Resultado_Jurisdiccion', 'Resultado_Mediopago', 'Resultado_persona', 'Resultado']
    counts = pd.concat([df_filtrado[col].value_counts() for col in df_filtrado.columns if col in columnas_contar], axis=1).fillna(0)

    fig, ax = plt.subplots()
    ax.pie(counts.sum(axis=1), labels=counts.index, autopct='%1.1f%%', startangle=90)
    ax.set_title('Segmentacion')
    ax.axis('equal')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    context = {'imgdata': uri}

    # Adjuntar el gráfico y el archivo al correo
    subject = 'Segmentacion'
    mensaje = 'Segmentacion'
    # from_email = 'notificaciones@riesgos365.com'
    # recipient_list = ['contacto@omenlaceglobal.co']
    from_email = 'quilesxasterin8@gmail.com'
    recipient_list = ['quilesxasterin8@gmail.com']
    email = EmailMessage(subject, mensaje, from_email, recipient_list)

    # Adjuntar el gráfico al correo
    email.attach('Distribucion_Segmentacion.png', buf.getvalue(), 'image/png')

    # Guardar el archivo de alarmas en la carpeta de archivos
    fecha_actual = timezone.now()
    carpeta = 'segmentacion'
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    nombre_archivo = f'Segmentacion_{fecha_actual.strftime("%Y%m%d%H%M%S")}.xlsx'
    ruta_completa = os.path.join(carpeta, nombre_archivo)
    df_filtrado.to_excel(ruta_completa, index=False)

    # Adjuntar el archivo al correo
    with open(ruta_completa, 'rb') as file:
        email.attach(nombre_archivo, file.read(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    email.send()
    plt.close()

    return nombre_archivo

# df_gen = pd.read_excel('D:/descargas/GENERALES.xlsx', sheet_name='CIIU')
# df_actual = pd.read_excel('D:/descargas/CLIENTES_.xlsx')

# segmentacion_c(df_actual, df_gen)