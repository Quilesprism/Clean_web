import pandas as pd


df_gen = pd.read_excel('D:/descargas/GENERALES.xlsx')

df=pd.read_excel('D:/descargas/CLIENTES_.xlsx')

result = pd.merge(df, df_gen[['CIIU', 'Valor_Asociado']], left_on='CIIU', right_on='CIIU', how='left')

result['Resultado'] = result['CIIU'] * (result['Valor'] * 0.1)