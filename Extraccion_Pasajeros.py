import pandas as pd
import requests
import PyPDF2
import os
import shutil
import time
import webbrowser

# Pagina web desde donde extraemos la informacion
path='http://www.jac.gob.cl/wp-content/uploads/'

#Creamos las rutas y carpetas donde quedará alocada la información de los vuelos y el path del directorio en el que trabajaremos

descargas= input("Indique la ruta donde se descargan los archivos: ")
nueva_ruta = input("Indique la ruta donde se moveran los archivos descargados: ")
ruta_archivo_pasajeros= input("Indique la ruta completa, incluyendo en nombre del archivo consolidado que se va a "
                              "generar (Incluir formato .csv, xlsx, etc) : ")


# Se crea el dataframe para agregar la data:
pasajeros_df = pd.DataFrame(columns=["Aerolinea","Origen","Destino","Entradas","Salidas","Fecha","Tipo_Vuelo"])

# Creamos una lista con todos los nombres y combinaciones de los archivos que serán descargados. Esto nos ayuda
# con la iteración de los valores más adelante

reportes=[['2019/02/','ResumenMensualEstadisticasEnero2019.xls','01-01-2019'],
          ['2019/02/','ResumenMensualEstadisticasFebrero2019.xls','01-02-2019'],
          ['2019/04/','ResumenMensualEstadisticasMarzo2019.xls','01-03-2019'],
          ['2019/02/','ResumenMensualEstadisticasAbril2019.xls','01-04-2019'],
          ['2019/02/','ResumenMensualEstadisticasMayo2019.xls','01-05-2019'],
          ['2019/02/','ResumenMensualEstadisticasJunio2019.xls','01-06-2019'],
          ['2019/02/','ResumenMensualEstadisticasJulio2019.xls','01-07-2019'],
          ['2019/02/','ResumenMensualEstadisticasAgosto2019.xls','01-08-2019'],
          ['2019/02/','ResumenMensualEstadisticasSeptiembre2019-2.xls','01-09-2019'],
          ['2019/11/','ResumenMensualEstadisticasOctubre2019.xls','01-10-2019'],
          ['2019/12/','ResumenMensualEstadisticasNoviembre2019.xls','01-11-2019'],
          ['2020/01/','13.-ResumenMensualEstadisticasDiciembre2019.xls','01-12-2019'],

          ['2020/02/','ResumenMensualEstadisticasEnero2020.xls','01-01-2020'],
          ['2020/03/','ResumenMensualEstadisticasFebrero2020.xls','01-02-2020'],
          ['2020/04/','ResumenMensualEstadisticasMarzo2020.xls','01-03-2020'],
          ['2020/05/','ResumenMensualEstadisticasAbril2020.xls','01-04-2020'],
          ['2020/06/','ResumenMensualEstadisticasMayo2020.xls','01-05-2020'],
          ['2020/07/','ResumenMensualEstadisticasJunio2020.xls','01-06-2020'],
          ['2020/08/','ResumenMensualEstadisticasJulio2020.xls','01-07-2020'],
          ['2020/09/','ResumenMensualEstadisticasAgosto2020.xls','01-08-2020'],
          ['2020/10/','ResumenMensualEstadisticasSeptiembre2020.xls','01-09-2020'],
          ['2020/12/','ResumenMensualEstadisticasOctubre2020.xls','01-10-2020'],
          ['2020/12/','ResumenMensualEstadisticasNoviembre2020.xls','01-11-2020'],
          ['2021/01/','ResumenMensualEstadisticasDiciembre2020.xls','01-12-2020'],

          ['2021/02/','ResumenMensualEstadisticasEnero2021.xls','01-01-2021'],
          ['2021/03/','ResumenMensualEstadisticasFebrero2021.xls','01-02-2021'],
          ['2021/04/','ResumenMensualEstadisticasMarzo2021.xls','01-03-2021'],
          ['2021/05/','ResumenMensualEstadisticasAbril2021.xls','01-04-2021'],
          ['2021/06/','ResumenMensualEstadisticasMayo2021.xls','01-05-2021'],
          ['2021/07/','ResumenMensualEstadisticasJunio2021.xls','01-06-2021'],
          ['2021/08/','ResumenMensualEstadisticasJulio2021.xls','01-07-2021'],
          ['2021/09/','ResumenMensualEstadisticasAgosto2021.xls','01-08-2021'],
          ['2021/10/','ResumenMensualEstadisticasSeptiembre2021.xls','01-09-2021'],
          ['2021/11/','ResumenMensualEstadisticasOctubre2021.xls','01-10-2021'],
          ['2021/12/','ResumenMensualEstadisticasNoviembre2021.xls','01-11-2021'],
          ['2022/01/','ResumenMensualEstadisticasDiciembre2021.xls','01-12-2021'],

          ['2022/02/','13.-ResumenMensualEstadisticasEnero2022.xls','01-01-2022'],
          ['2022/03/','ResumenMensualEstadisticasFebrero2022.xls','01-02-2022'],
          ['2022/04/','ResumenMensualEstadisticasMarzo2022.xls','01-03-2022'],
          ['2022/05/','ResumenMensualEstadisticasAbril2022.xls','01-04-2022'],
          ['2022/06/','ResumenMensualEstadisticasMayo2022.xls','01-05-2022'],
          ['2022/07/','ResumenMensualEstadisticasJunio2022.xls','01-06-2022'],
          ['2022/08/','ResumenMensualEstadisticasJulio2022.xls','01-07-2022'],
          ['2022/09/','ResumenMensualEstadisticasAgosto2022.xls','01-08-2022'],
          ['2022/10/','ResumenMensualEstadisticasSeptiembre2022.xls','01-09-2022'],
          ['2022/11/','ResumenMensualEstadisticasOctubre2022.xls','01-10-2022'],
          ['2022/12/','ResumenMensualEstadisticasNoviembre2022.xls','01-11-2022'],
          ['2023/01/','ResumenMensualEstadisticasDiciembre2022.xls','01-12-2022'],

          ['2023/02/','ResumenMensualEstadisticasEnero2023.xls','01-01-2023'],
          ['2023/03/','ResumenMensualEstadisticasFebrero2023.xls','01-02-2023'],
          ['2023/04/','ResumenMensualEstadisticasMarzo2023.xls','01-03-2023']]


# Iniciamos el loop

for dato in reportes:
    # Se descarga el archivo y se envía a la carpeta objetivo

    ruta = f'{path}{dato[0]}{dato[1]}'
    webbrowser.open(ruta)
    time.sleep(15)
    shutil.move(f'{descargas}{dato[1]}', f'{nueva_ruta}{dato[1]}')
    time.sleep(10)

    # Vamos a extraer la data para cada uno de los archivos
    # Primero los vuelos internacionales
    # Aquí abrimos el archivo, tomamos las columnas que necesitamos y modificamos el dataset para agregarlo al consolidado

    # Primero lo hacemos con los vuelos nacionales

    pasajeros_int_df = pd.read_excel(f'{nueva_ruta}{dato[1]}', sheet_name="INT3", skiprows=4, header=1)
    pasajeros_int_df = pasajeros_int_df[["OPERADORES", "ORIGEN", "DESTINO", "LLEGAN.3", "SALEN.3"]]
    pasajeros_int_df['OPERADORES'].fillna(method='ffill', inplace=True)
    pasajeros_int_df.dropna(subset=['OPERADORES'], inplace=True)
    pasajeros_int_df = pasajeros_int_df.iloc[
                       :(pasajeros_int_df[pasajeros_int_df['OPERADORES'].str.find("KILOGRAMOS") != -1].index.min())]
    pasajeros_int_df = pasajeros_int_df[pasajeros_int_df['OPERADORES'].str.find("Total") == -1]
    pasajeros_int_df = pasajeros_int_df[pasajeros_int_df['OPERADORES'].str.find("TOTAL") == -1]
    pasajeros_int_df = pasajeros_int_df[pasajeros_int_df['OPERADORES'].str.find("TRAFICO") == -1]
    pasajeros_int_df = pasajeros_int_df[pasajeros_int_df['OPERADORES'].str.find("OPERADORES") == -1]
    pasajeros_int_df["Fecha"] = dato[2]
    pasajeros_int_df = pasajeros_int_df.rename(
        columns={"OPERADORES": "Aerolinea", "ORIGEN": "Origen", "DESTINO": "Destino",
                 "LLEGAN.3": "Entradas","SALEN.3": "Salidas","Fecha": "Fecha"})
    pasajeros_int_df["Tipo_Vuelo"] = "Internacional"

    # Seguimos con los vuelos nacionales
    pasajeros_nac_df = pd.read_excel(f'{nueva_ruta}{dato[1]}', sheet_name="NAC3", skiprows=4, header=1)
    pasajeros_nac_df = pasajeros_nac_df[["OPERADORES", "ORIGEN", "DESTINO", "LLEGAN.3", "SALEN.3"]]
    pasajeros_nac_df['OPERADORES'].fillna(method='ffill', inplace=True)
    pasajeros_nac_df.dropna(subset=['OPERADORES'], inplace=True)
    pasajeros_nac_df = pasajeros_nac_df.iloc[
                       :(pasajeros_nac_df[pasajeros_nac_df['OPERADORES'].str.find("KILOGRAMOS") != -1].index.min())]
    pasajeros_nac_df = pasajeros_nac_df[pasajeros_nac_df['OPERADORES'].str.find("Total") == -1]
    pasajeros_nac_df = pasajeros_nac_df[pasajeros_nac_df['OPERADORES'].str.find("TOTAL") == -1]
    pasajeros_nac_df = pasajeros_nac_df[pasajeros_nac_df['OPERADORES'].str.find("TRAFICO") == -1]
    pasajeros_nac_df = pasajeros_nac_df[pasajeros_nac_df['OPERADORES'].str.find("OPERADORES") == -1]
    pasajeros_nac_df["Fecha"] = dato[2]
    pasajeros_nac_df = pasajeros_nac_df.rename(
        columns={"OPERADORES": "Aerolinea", "ORIGEN": "Origen", "DESTINO": "Destino",
                 "LLEGAN.3": "Entradas", "SALEN.3": "Salidas", "Fecha": "Fecha"})
    pasajeros_nac_df["Tipo_Vuelo"]="Nacional"

    # Concatenamos los datasets
    pasajeros_df = pd.concat([pasajeros_df, pasajeros_int_df, pasajeros_nac_df])

# Luego ajustamos el nombre de las aerolíneas a minúsculas
pasajeros_df["Aerolinea"] = pasajeros_df["Aerolinea"].apply(lambda x: x.lower())

# Guardamos el archivo como un excel
pasajeros_df.to_csv(ruta_archivo_pasajeros, sep="|", index=False, header=True)


