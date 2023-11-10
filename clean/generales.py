
df['Concatenado'] = df['DEPARTAMENTO'].astype(str) + df['CIUDAD'].astype(str)
df_generales['Concatenado'] = df_generales['Departamento'].astype(str) + df_generales['Municipio'].astype(str)

ciudades_cliente = df['CIUDAD'].unique()

for ciudad in ciudades_cliente:
    departamento_correspondiente = df_generales[df_generales['Municipio'] == ciudad]['Departamento'].values

    if len(departamento_correspondiente) > 0:
        df.loc[df['CIUDAD'] == ciudad, 'SinCorr_Ciudad'] = departamento_correspondiente[0]

df['SinCorrespondencia'] = df['Concatenado'].apply(lambda x: 0 if x in df_generales['Concatenado'].values else 1)

