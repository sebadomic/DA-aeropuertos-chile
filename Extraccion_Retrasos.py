import pandas as pd
import requests
import PyPDF2
import os
import tabula

# Esta función la utilizaremos más adelante para modificar los DF consolidados
def aero_reemplazar_terminos(df):
    df["puntualidad"] = df["puntualidad"].str.replace("%", "")
    df["puntualidad"] = df["puntualidad"].str.replace(",", ".")
    df["puntualidad"] = pd.to_numeric(df["puntualidad"]) / 100

    df["vuelos_regulares"] = df["vuelos_regulares"].str.replace("%", "")
    df["vuelos_regulares"] = df["vuelos_regulares"].str.replace(",", ".")
    df["vuelos_regulares"] = pd.to_numeric(df["vuelos_regulares"]) / 100

    return df

# Generamos un DF para ir anexando la data
Aero_Cons= pd.DataFrame(columns=['aerolinea','numero_vuelos','puntualidad','minutos_atraso','vuelos_regulares'])

#Creamos la carpeta donde quedará alocada la información de los vuelos y el path del directorio en el que trabajaremos
parent_dir= input("Indique la ruta donde se moveran los archivos descargados: ")

# Hacemos una lista con las aerolíneas y los destinos que aparecen en los archivos PDF
Aerolineas= ['Sky Airline','Amaszonas S.A.','Grupo LATAM','JetSmart Spa','JetSmart','Amaszonas Paraguay','Pisco PerÃº',
             'Amaszonas','Latin American Wings','Aerolineas Argentinas','Star Up S.A.','Copa Air','Avianca','Gol Trans',
             'American Airlines','Oceanair Linhas Aereas','Air Canada','Delta Air','Aeromexico','Air France','Iberia',
             'United Airlines','K.L.M.','Alitalia','Lacsa','Qantas Airways','British Airways','Austral',
             'Plus Ultra Lineas Aereas','Estelar Latinoamerica','Otras Aerolineas','Dynamic Airways','Emirates','Taca-Lacsa',
             'Jetsmart Airlines S.A.','Aerolineas Argentinas-Austral','Grupo Avianca','Iberia-Level','Aero. Argentinas-Austral',
             'Conviasa','Star Up Sa','LATAM','Aerolineas Argentinas','Air Canada','Aeromexico','Air France','Alitalia',
             'Aerolineas Argentinas-Austral','Aero. Argentinas-Austral']

Destinos= ['Florianapolis', 'Ciudad de Panama', 'Asuncion', 'Houston', 'Cartagena, Colombia', 'Dallas', 'Bariloche',
'Guayaquil', 'Atlanta', 'Bogota', 'Montevideo', 'Cordoba', 'Miami', 'Mendoza', 'Ciudad de Mexico', 'Rio de Janeiro',
'Nueva York', 'Sao Paulo', 'Lima', 'Buenos Aires', 'Paris', 'Curitiba, Bra.', 'Toronto', 'Otras Ciudades', 'Madrid',
'Los Angeles', 'Barcelona', 'Trujillo', 'Auckland N.Z.', 'Medellin', 'Cali', 'Londres', 'Sydney', 'Copiapo', 'Balmaceda',
'Osorno','Calama','Arica','Puerto Natales','Antofagasta','Concepcion','Iquique','Punta Arenas','Temuco','Puerto Montt',
'La Serena','Valdivia','Castro (Chiloe)','Isla de Pascua','Santiago','Cusco','Tacna','Puerto Principe', 'Santa Cruz',
'Salta Arg.','La Paz','Barranquilla','Caracas','Santa Genoveva, Bra.','Papeete','Rio Gallegos Arg.','Puerto Stanley',
'Ushuia','Roma', 'El Palomar Arg.', 'Salvador Bahia', 'Quito', 'Latinoamericanas', 'Norteamericanas', 'Europeas',
'Pacifico Sur','Latinoamericanos','Norteamericanos','Europeos','Pcifico Sur','Arequipa','Cancun','Punta Cana','Porto Alegre']


# Armamos la lista para los pdf que son excepciones para la ciudad de Santiago
EXCEPCION_STGO= ['Santiago-Abr-Jun-2020','Santiago-Jul-Sep-2020','Santiago-Oct-Dic-2020','Santiago-Ene-Mar-2021',
                 'Santiago-Abr-Jun-2021','Santiago-Jul-Sep-2021','Santiago-Oct-Dic-2021','Santiago-Ene-Mar-2022']

# HACEMOS LOS LISTADOS DE CIUDADES Y LOS PERIODOS PARA BAJAR LA DATA
CIUDADES = {'Arica':'Arica',
            'Iquique':'Iquique','Antofagasta':'Antofagasta','Calama':'Calama',
            'Copiapo':'Copiapo','la-serena':'LaSerena','isla-de-pascua':'IslaDePascua',
            'santiago':'Santiago','concepcion':'Concepcion','temuco':'Temuco','valdivia':'Valdivia',
            'osorno':'Osorno','puerto-montt':'PuertoMontt','balmaceda':'Balmaceda',
            'puerto-natales':'PuertoNatales','castro-chiloe':'Castro','punta-arenas':'PuntaArenas'
            }

PERIODOS= [['2020/04/','-Ene-Mar-2020','01-01-2020'],
           ['2020/07/','-Abr-Jun-2020','01-04-2020'],
           ['2020/10/','-Jul-Sep-2020','01-07-2020'],
           ['2021/01/','-Oct-Dic-2020','01-10-2020'],
           ['2021/04/','-Ene-Mar-2021','01-01-2021'],
           ['2021/07/','-Abr-Jun-2021','01-04-2021'],
           ['2021/10/','-Jul-Sep-2021','01-07-2021'],
           ['2022/01/','-Oct-Dic-2021','01-10-2021'],
           ['2022/04/','-Ene-Mar-2022','01-01-2022'],
           ['2022/07/','-Abr-Jun-2022','01-04-2022'],
           ['2022/10/','-Jul-Sep-2022','01-07-2022'],
           ['2023/01/','-Oct-Dic-2022','01-10-2022'],
           ['2023/04/','-Ene-Mar-2023','01-01-2023']
]

# HACEMOS EL LOOP PARA BAJAR LAS CIUDADES Y LOS PERIODOS
for a,b in CIUDADES.items():
    #ESTABLECEMOS EL DIRECTORIO EN EL QUE QUEDARÁ ALOCADO
    folder=b
    path=os.path.join(parent_dir,folder)
    os.mkdir(path)

    for fecha in PERIODOS:
        # Define la URL del archivo PDF que vamos a descargar
        # Puerto Natales tiene una exepción, la que colocamos en el siguiente IF
        if (fecha[0] == '2014/10/') and (fecha[1] == '-Ene-Mar-2019') and (b == 'PuertoNatales'):
            url = f'http://www.jac.gob.cl/wp-content/uploads/2019/02/{b}{fecha[1]}.pdf'
        else:
            url = f'http://www.jac.gob.cl/wp-content/uploads/{fecha[0]}/{b}{fecha[1]}.pdf'
        # Pedimos una respuesta de la URL para bajar el archivo
        response = requests.get(url)

        # Abrimos un nuevo comando para guardar el archivo PDF
        with open(f'{path}/{b}{fecha[1]}.pdf', "wb") as f:
            f.write(response.content)
        # Si el archivo pesa menos de 1 kb (Error), lo borramos
        if os.path.getsize(f'{path}/{b}{fecha[1]}.pdf') < 260:
            os.remove(f'{path}/{b}{fecha[1]}.pdf')
        else:
            pass

        # Si existe, abrimos el archivo y extraemos las tablas correspondientes
        if os.path.isfile(f'{path}/{b}{fecha[1]}.pdf') is True:

            tabula.convert_into(f'{path}/{b}{fecha[1]}.pdf', f'{b}{fecha[1]}.csv', output_format="csv", pages=1)
            tabla = pd.read_csv(f'{b}{fecha[1]}.csv', skiprows=3, header=None, encoding='latin-1')
            tabla = tabla.rename(columns={0: 'aerolinea', 1: 'numero_vuelos', 2: 'puntualidad',
                                              3: 'minutos_atraso', 4: 'vuelos_regulares'})
            tabla['fecha']= fecha[2]
            tabla['aeropuerto']= b
            tabla["numero_vuelos"].fillna(0, inplace=True)
            tabla["numero_vuelos"] = tabla["numero_vuelos"]
            Aero_Cons= pd.concat([Aero_Cons,tabla])
            os.remove(f'{b}{fecha[1]}.csv')
        else:
            pass
    print(f'Se ha descargado la información de {b}')


# Hacemos el caso de Santiago y sus PDF especiales
path_stgo='C:/Users/srram/Proyectos_Data_Science/Análisis_Aeropuertos/data/retrasos/Santiago'
for fecha in PERIODOS:
    if os.path.isfile(f'{path_stgo}/Santiago{fecha[1]}.pdf') is True:
        if f'Santiago{fecha[1]}' in EXCEPCION_STGO:
            tabula.convert_into(f'{path_stgo}/Santiago{fecha[1]}.pdf', f'Santiago{fecha[1]}.csv', output_format="csv", pages=2)
            tabla = pd.read_csv(f'Santiago{fecha[1]}.csv', skiprows=3,  header=None, encoding='latin-1')
            tabla = tabla.rename(columns={0: 'aerolinea', 1: 'numero_vuelos', 2: 'puntualidad',
                                          3: 'minutos_atraso', 4: 'vuelos_regulares'})
            tabla['fecha'] = fecha[2]
            tabla['aeropuerto'] = 'Santiago'
            tabla["numero_vuelos"].fillna(0, inplace=True)
            tabla["numero_vuelos"] = tabla["numero_vuelos"]
            Aero_Cons = pd.concat([Aero_Cons, tabla])
            os.remove(f'Santiago{fecha[1]}.csv')
        else:
            tabula.convert_into(f'{path_stgo}/Santiago{fecha[1]}.pdf', f'Santiago{fecha[1]}.csv', output_format="csv",
                                pages=5)
            tabla = pd.read_csv(f'Santiago{fecha[1]}.csv', skiprows=3, header=None, encoding='latin-1')
            tabla = tabla.rename(columns={0: 'aerolinea', 1: 'numero_vuelos', 2: 'puntualidad',
                                          3: 'minutos_atraso', 4: 'nula', 5:'vuelos_regulares'})
            tabla.drop(['nula'], axis=1, inplace=True)
            tabla['fecha'] = fecha[2]
            tabla['aeropuerto'] = 'Santiago'
            tabla = tabla[(tabla["aerolinea"] != "INTERNACIONAL")]
            tabla = tabla[(tabla["aerolinea"] != "NACIONAL")]
            tabla["numero_vuelos"].fillna(0, inplace=True)
            tabla["numero_vuelos"] = tabla["numero_vuelos"]

            Aero_Cons = pd.concat([Aero_Cons, tabla])
            os.remove(f'Santiago{fecha[1]}.csv')
    else:
        pass
print('Se ha terminado la descarga de Santiago')

# Separamos la data por ciudades de destino y por aeropuerto
Dest_Cons= Aero_Cons[Aero_Cons['aerolinea'].isin(Destinos)]
Aero_Cons= Aero_Cons[Aero_Cons['aerolinea'].isin(Aerolineas)]

# Trabajamos primero con la data de las aerolineas y luego los destinos
# Hacemos los ajustes en la información de las aerolíneas (al leer desde un PDF quedan errores en los valores numéricos)
Aero_Cons= aero_reemplazar_terminos(Aero_Cons)
Aero_Cons["minutos_atraso"].fillna(0, inplace=True)
Aero_Cons.reset_index(drop=True, inplace=True)
Aero_Cons["numero_vuelos"]= Aero_Cons["numero_vuelos"].astype(str)
Aero_Cons['numero_vuelos'] = Aero_Cons['numero_vuelos'].apply(lambda x: x[:-2] if x[-2::] == ".0" else x)
Aero_Cons['numero_vuelos'] = Aero_Cons['numero_vuelos'].apply(lambda x: x.replace('.',''))
Aero_Cons['numero_vuelos'] = Aero_Cons['numero_vuelos'].astype(int)
Aero_Cons["numero_vuelos"].fillna(0, inplace=True)


# Continuamos con la información de los destinos

Dest_Cons= aero_reemplazar_terminos(Dest_Cons)
Dest_Cons["minutos_atraso"].fillna(0, inplace=True)
Dest_Cons.reset_index(drop=True, inplace=True)
Dest_Cons["numero_vuelos"]= Dest_Cons["numero_vuelos"].astype(str)
Dest_Cons['numero_vuelos'] = Dest_Cons['numero_vuelos'].apply(lambda x: str(1130) if x == "1.13" else x)
Dest_Cons['numero_vuelos'] = Dest_Cons['numero_vuelos'].apply(lambda x: str(1040) if x == "1.04" else x)
Dest_Cons['numero_vuelos'] = Dest_Cons['numero_vuelos'].apply(lambda x: x[:-2] if x[-3::] == "0.0" else x)
Dest_Cons['numero_vuelos'] = Dest_Cons['numero_vuelos'].apply(lambda x: x[:-2] if x[-2::] == ".0" else x)
Dest_Cons['numero_vuelos'] = Dest_Cons['numero_vuelos'].apply(lambda x: x.replace('.',''))
Dest_Cons['numero_vuelos'] = Dest_Cons['numero_vuelos'].astype(int)
Dest_Cons["numero_vuelos"].fillna(0, inplace=True)

Dest_Cons = Dest_Cons.rename(columns={'aerolinea':'destino'})


# Guardamos en un archivo excel los destinos y las aerolineas
Aero_Cons.to_csv("data/consolidados/Restrasos_Aerolineas_Consolidadas.csv", sep="|", index=False, header=True)
Dest_Cons.to_csv("data/consolidados/Restrasos_Destinos_Consolidados.csv", sep="|", index=False, header=True)


