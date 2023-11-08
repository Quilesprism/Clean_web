import os
import pandas as pd
import calendar
import re
from datetime import datetime
import unidecode
from django.core.mail import send_mail

def limpiar_dataframe(df):
    errores = {}  
    try:
        def registrar_error(columna, tipo_error):
            if columna in errores:
                if tipo_error in errores[columna]:
                    errores[columna][tipo_error] += 1
                else:
                    errores[columna][tipo_error] = 1
            else:
                errores[columna] = {tipo_error: 1}
        df['FECHA TRANSACCION'] = pd.to_datetime(df['FECHA TRANSACCION'], errors='coerce', dayfirst=True)
        valid_dates = df.dropna(subset=['FECHA TRANSACCION'])
        mode_year = valid_dates['FECHA TRANSACCION'].dt.year.mode()[0]
        mode_month = valid_dates['FECHA TRANSACCION'].dt.month.mode()[0]
        for i, date in enumerate(df['FECHA TRANSACCION']):
            if pd.isna(date):
                _, last_day_of_month = calendar.monthrange(mode_year, mode_month)
                df.loc[i, 'FECHA TRANSACCION'] = datetime(mode_year, mode_month, last_day_of_month)
                
        def limpiar_columna(col):
            if isinstance(col, str) == ' ' or pd.isnull(col) or col == 'N/A':
                return "NOMBRE_EMPRESA"
            else:
                return col
        df['NOMBRE DEL FUNCIONARIO RESPONSABLE DE LA VENTA'] = df['NOMBRE DEL FUNCIONARIO RESPONSABLE DE LA VENTA'].apply(limpiar_columna)
        
        columnas_a_limpiar = ['NOMBRE', 'NOMBRE DEL FUNCIONARIO RESPONSABLE DE LA VENTA', 'PAIS', 'CIUDAD', 'DEPARTAMENTO']
        
        df[columnas_a_limpiar] = df[columnas_a_limpiar].apply(lambda col: col.str.replace('[Ññ]', '|', regex=True))
        
        def limpiar_centro(centro):
            if isinstance(centro, str) == ' ' or pd.isnull(centro) or centro == 'N/A':
                return 1000
            else:
                return centro
            
        df['ID CENTRO COSTOS'] = df['ID CENTRO COSTOS'].apply(limpiar_centro)
        
        def limpiar_nombre(nombre):
            if isinstance(nombre, str):
                nombre = unidecode.unidecode(nombre)
                nombre = re.sub('[^A-Z0-9&| ]+', '', nombre.upper())
                nombre = nombre.replace('|', 'Ñ')
                nombre = re.sub(' +', ' ', nombre).strip()
                return nombre
            else:
                return None
        df[columnas_a_limpiar] = df[columnas_a_limpiar].apply(lambda x: x.map(limpiar_nombre))
        def aplicar_regla_pais(row):
            if row['PAIS'] != 'COLOMBIA':
                row['CIUDAD'] = row['PAIS']
                row['DEPARTAMENTO'] = 'EXTRANJERO'
            return row
        df = df.apply(aplicar_regla_pais, axis=1)
        df['Concatenado'] = df['DEPARTAMENTO'].astype(str) + df['CIUDAD'].astype(str)
        def limpiar_nit(nit):
            nit = str(nit)
            nit = re.sub('[^0-9-]', '', nit)  
            partes = nit.split('-')
            if len(partes) > 1 and len(partes[1]) <= 3: 
                nit = partes[0]  
            if nit == '':
                return  
            return int(nit)  
        df['No. DOCUMENTO DE IDENTIDAD'] = df['No. DOCUMENTO DE IDENTIDAD'].apply(limpiar_nit)
        df['CIIU'] = pd.to_numeric(df['CIIU'], errors='coerce')
        df['CIIU'].fillna(9999, inplace=True)
        df['CIIU'] = df['CIIU'].astype(int)
        df['VALOR DE LA TRANSACCION'] = df['VALOR DE LA TRANSACCION'].replace('', 0)
        def determinar_tipo_persona(nit):
            try:
                primer_digito = int(str(nit)[0])

                if primer_digito > 7:
                    return 'JURIDICA'
                elif primer_digito <= 7:
                    return 'NATURAL'
            except (ValueError, TypeError) as e:
                tipo_error = type(e)._name_
                mensaje_error = str(e)
                registrar_error('No. DOCUMENTO DE IDENTIDAD', tipo_error)
                #enviar_correo_electronico(f"Error al limpiar el DataFrame: {mensaje_error}")

        # Aplica la función a la columna 'No. DOCUMENTO DE IDENTIDAD' y asigna los resultados a la columna 'TIPO PERSONA'
        df['TIPO PERSONA (natural/jurídica)'] = df['No. DOCUMENTO DE IDENTIDAD'].apply(lambda x: x if x in ['NATURAL', 'JURIDICA'] else determinar_tipo_persona(x))

        df['MEDIO PAGO'] = df['MEDIO PAGO'].apply(lambda x: 'TRANSFERENCIA' if pd.isna(x) or (x != 'EFECTIVO' and x.strip().upper() != 'EFECTIVO') else 'EFECTIVO')

        return df

    except Exception as e:
        tipo_error = type(e).__name__  
        mensaje_error = str(e) 
        guardar_errores_en_txt(tipo_error)
        enviar_correo_electronico(f"Error al limpiar el DataFrame: {mensaje_error}")

def limpiar_Proveedor(df):
    errores = {}  
    try:
        def registrar_error(columna, tipo_error):
            if columna in errores:
                if tipo_error in errores[columna]:
                    errores[columna][tipo_error] += 1
                else:
                    errores[columna][tipo_error] = 1
            else:
                errores[columna] = {tipo_error: 1}
        df['FECHA TRANSACCION'] = pd.to_datetime(df['FECHA TRANSACCION'], errors='coerce', dayfirst=True)
        valid_dates = df.dropna(subset=['FECHA TRANSACCION'])
        mode_year = valid_dates['FECHA TRANSACCION'].dt.year.mode()[0]
        mode_month = valid_dates['FECHA TRANSACCION'].dt.month.mode()[0]
        for i, date in enumerate(df['FECHA TRANSACCION']):
            if pd.isna(date):
                _, last_day_of_month = calendar.monthrange(mode_year, mode_month)
                df.loc[i, 'FECHA TRANSACCION'] = datetime(mode_year, mode_month, last_day_of_month)
                
        def limpiar_columna(col):
            if isinstance(col, str) == ' ' or pd.isnull(col) or col == 'N/A':
                return "NOMBRE_EMPRESA"
            else:
                return col
        columnas_a_limpiar = ['NOMBRE', 'PAIS', 'CIUDAD', 'DEPARTAMENTO']
        
        df[columnas_a_limpiar] = df[columnas_a_limpiar].apply(lambda col: col.str.replace('[Ññ]', '|', regex=True))
        
        def limpiar_centro(centro):
            if isinstance(centro, str) == ' ' or pd.isnull(centro) or centro == 'N/A':
                return 1000
            else:
                return centro
            
        df['ID CENTRO COSTOS'] = df['ID CENTRO COSTOS'].apply(limpiar_centro)
        
        def limpiar_nombre(nombre):
            if isinstance(nombre, str):
                nombre = unidecode.unidecode(nombre)
                nombre = re.sub('[^A-Z0-9&| ]+', '', nombre.upper())
                nombre = nombre.replace('|', 'Ñ')
                nombre = re.sub(' +', ' ', nombre).strip()
                return nombre
            else:
                return None
        df[columnas_a_limpiar] = df[columnas_a_limpiar].apply(lambda x: x.map(limpiar_nombre))
        def aplicar_regla_pais(row):
            if row['PAIS'] != 'COLOMBIA':
                row['CIUDAD'] = row['PAIS']
                row['DEPARTAMENTO'] = 'EXTRANJERO'
            return row
        df = df.apply(aplicar_regla_pais, axis=1)
        df['Concatenado'] = df['DEPARTAMENTO'].astype(str) + df['CIUDAD'].astype(str)
        def limpiar_nit(nit):
            nit = str(nit)
            nit = re.sub('[^0-9-]', '', nit)  
            partes = nit.split('-')
            if len(partes) > 1 and len(partes[1]) <= 3: 
                nit = partes[0]  
            if nit == '':
                return  
            return int(nit)  
        df['No. DOCUMENTO DE IDENTIDAD'] = df['No. DOCUMENTO DE IDENTIDAD'].apply(limpiar_nit)
        df['CIIU'] = pd.to_numeric(df['CIIU'], errors='coerce')
        df['CIIU'].fillna(9999, inplace=True)
        df['CIIU'] = df['CIIU'].astype(int)
        df['VALOR DE LA TRANSACCION'] = df['VALOR DE LA TRANSACCION'].replace('', 0)
        def determinar_tipo_persona(nit):
            try:
                primer_digito = int(str(nit)[0])

                if primer_digito > 7:
                    return 'JURIDICA'
                elif primer_digito <= 7:
                    return 'NATURAL'
            except (ValueError, TypeError) as e:
                tipo_error = type(e)._name_
                mensaje_error = str(e)
                registrar_error('No. DOCUMENTO DE IDENTIDAD', tipo_error)
                #enviar_correo_electronico(f"Error al limpiar el DataFrame: {mensaje_error}")

        # Aplica la función a la columna 'No. DOCUMENTO DE IDENTIDAD' y asigna los resultados a la columna 'TIPO PERSONA'
        df['TIPO PERSONA (natural/jurídica)'] = df['No. DOCUMENTO DE IDENTIDAD'].apply(lambda x: x if x in ['NATURAL', 'JURIDICA'] else determinar_tipo_persona(x))

        df['MEDIO PAGO'] = df['MEDIO PAGO'].apply(lambda x: 'TRANSFERENCIA' if pd.isna(x) or (x != 'EFECTIVO' and x.strip().upper() != 'EFECTIVO') else 'EFECTIVO')

        return df

    except Exception as e:
        tipo_error = type(e).__name__  
        mensaje_error = str(e) 
        guardar_errores_en_txt(tipo_error)
        enviar_correo_electronico(f"Error al limpiar el DataFrame: {mensaje_error}")


def guardar_errores_en_txt(errores):
    archivo_errores = 'errores.txt'
    carpeta_errores = 'errores'
    if not os.path.exists(carpeta_errores):
        os.makedirs(carpeta_errores)
    ruta_errores = os.path.join(carpeta_errores, archivo_errores)
    with open(ruta_errores, 'w') as archivo_errores:
        archivo_errores.write("Errores en la limpieza del DataFrame:\n")
        for columna, errores_columna in errores.items():
            archivo_errores.write(f"Columna: {columna}\n")
            for tipo_error, conteo in errores_columna.items():
                archivo_errores.write(f"  Tipo de error: {tipo_error}, Conteo: {conteo}\n")


def enviar_correo_electronico(mensaje):
    subject = 'Error en la aplicación'
    message = mensaje
    from_email = 'quilesxasterin8@gmail.com'
    recipient_list = ['quilesxasterin8@gmail.com']

    send_mail(subject, message, from_email, recipient_list)



# df=pd.read_excel('C:/Users/quile/Downloads/PROVEEDORES ENERO 2023.xlsx')

# limpiar_Proveedor(df)

# df.to_excel('excel.xlsx')

