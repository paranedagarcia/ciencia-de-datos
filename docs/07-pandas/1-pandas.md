---
id: pandas-datos
title: "Manipulación de datos"
sidebar_label: "Manipulación de datos"
sidebar_position: 2
description: "Manipulación de datos"
---



[![](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1K--o6d7H3VNMLnxwrWftPAWLiwTBByAm)


## Librería de manipulación de datos


## PANDAS SERIES
Una "Serie" es una estructura de una sola dimensión con:
- Datos (numéricos, texto, fechas, etc.)
- Índices (etiquetas únicas para cada valor, por defecto 0,1,2...)

Características clave:
- Homogénea (mismo tipo de dato)
- Índice personalizable
- Soporta operaciones matemáticas y lógicas


```python showLineNumbers
# carga de librerías
import warnings
import pandas as pd
import numpy as np

# Desactivar warnings en este notebook
warnings.filterwarnings('ignore')

# Evitar SettingWithCopyWarning de pandas
pd.options.mode.chained_assignment = None  # default='warn'

# Opcional: silenciar errores/warnings numéricos de numpy (inf/nan/div0)
#np.seterr(all='ignore')
```


```python showLineNumbers
# Desde una lista
s1 = pd.Series([10, 20, 30, 40])
print(s1)
```
```raw

    0    10
    1    20
    2    30
    3    40
    dtype: int64
```


```python showLineNumbers
# Con índices personalizados
s2 = pd.Series(['A', 'B', 'C'], index=['x', 'y', 'z'])
print(s2)
```
```raw
    x    A
    y    B
    z    C
    dtype: object
```


```python showLineNumbers
# Desde diccionario
s3 = pd.Series({'Manzana': 120, 'Banana': 80, 'Naranja': 60})
print(s3)
```
```raw
    Manzana    120
    Banana      80
    Naranja     60
    dtype: int64
```

### Acceso a los elementos


```python showLineNumbers
# creacion de una serie llamada 'serie'
serie = pd.Series([100, 200, 300,400, 500,600,700,800,900], 
                  index=['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep'])
```


```python showLineNumbers
# Por índice numérico
print(serie[2])
300
```


```python showLineNumbers
# acceso a un elemnto por posición
print(serie.iloc[0])
100
```

```python showLineNumbers
# Por etiqueta (indice)
print(serie['ene'])
100
```


```python showLineNumbers
# Slicing
print(serie['ene':'feb'])
```
```raw
    ene    100
    feb    200
    dtype: int64
```


```python showLineNumbers
# Condicional
print(serie[serie > 150])
```
```raw
    feb    200
    mar    300
    dtype: int64
```

### Algunas operaciones simples


```python showLineNumbers
# creamos 2 series, s1 y s2
s1 = pd.Series([1, 2, 3])
s2 = pd.Series([10, 20, 30])
```

```python showLineNumbers
# Suma
print(s1 + s2)
```
```raw
    0    11
    1    22
    2    33
    dtype: int64
```


```python showLineNumbers
# Multiplicación por escalar
print(s1 * 10)
```
```raw
    0    10
    1    20
    2    30
    dtype: int64
```


```python showLineNumbers
# Funciones matemáticas
print(s1.apply(lambda x: x**2))
```
```raw
    0    1
    1    4
    2    9
    dtype: int64
```


```python showLineNumbers
# Lógica
print(s1 > 1)
```
```raw
    0    False
    1     True
    2     True
    dtype: bool
```

### Algunos métodos útiles


```python showLineNumbers
# metodos útiles con series

s = pd.Series([1, 2, 2, 3, 3, 6,7,8,9,0,3, 4])
separador = '-' * 40  # caracter separador entre cada sentencia

print(f'{separador}\n Primeros 3 valores: \n{s.head(3)}')           # Primeros 3
print(f'{separador}\n Valores únicos dentro de la serie: \n {s.unique()}')          # Valores únicos: [1,2,3,4]
print(f'{separador}\n Cantidad de valores unicos: {s.nunique()}')         # Cantidad de únicos: 4
print(f'{separador}\n Frecuencias de valores: \n {s.value_counts()}')    # Frecuencias: 3→3, 2→2, 1→1, 4→1
print(f'{separador}\n Serie en orden ascendente: \n {s.sort_values()}')     # Orden ascendente
print(f'{separador}\n Serie ordenada por su índice: \n {s.sort_index()}')      # Orden por índice
```
```raw
    ----------------------------------------
     Primeros 3 valores: 
    0    1
    1    2
    2    2
    dtype: int64
    ----------------------------------------
     Valores únicos dentro de la serie: 
     [1 2 3 6 7 8 9 0 4]
    ----------------------------------------
     Cantidad de valores unicos: 9
    ----------------------------------------
     Frecuencias de valores: 
     3    3
    2    2
    1    1
    6    1
    7    1
    8    1
    9    1
    0    1
    4    1
    Name: count, dtype: int64
    ----------------------------------------
     Serie en orden ascendente: 
     9     0
    0     1
    2     2
    1     2
    4     3
    3     3
    10    3
    11    4
    5     6
    6     7
    7     8
    8     9
    dtype: int64
    ----------------------------------------
     Serie ordenada por su índice: 
     0     1
    1     2
    2     2
    3     3
    4     3
    5     6
    6     7
    7     8
    8     9
    9     0
    10    3
    11    4
    dtype: int64
```

## Pandas Dataframe

En un dataframe los datos se despliegan en forma bidimensional, en tablas, con columnas y filas (al estilo de Excel).


```python showLineNumbers
# Desde diccionario
datos = {
    'Nombre': ['Ana', 'Luis', 'María'],
    'Edad': [25, 30, 22],
    'Ciudad': ['STGO', 'Medellín', 'Guadalajara']
}

df = pd.DataFrame(datos)
print(df)
```
```raw
      Nombre  Edad       Ciudad
    0    Ana    25         STGO
    1   Luis    30     Medellín
    2  María    22  Guadalajara
```


```python showLineNumbers
# Desde lista de listas + nombres de columnas
df2 = pd.DataFrame([
    [1, 'A', True],
    [2, 'B', False]
], columns=['ID', 'Letra', 'Activo'])

print(df2)
```
```raw
       ID Letra  Activo
    0   1     A    True
    1   2     B   False
```

### Acceso a las filas


```python showLineNumbers
# Por etiqueta (si índice es 0,1,2)
print(df.loc[0])
```
```raw
    Nombre     Ana
    Edad        25
    Ciudad    STGO
    Name: 0, dtype: object
```


```python showLineNumbers
# Por posición
print(df.iloc[1])
```
```raw
    Nombre        Luis
    Edad            30
    Ciudad    Medellín
    Name: 1, dtype: object
```


```python showLineNumbers
# Rangos
print(df.loc[0:1])          # Filas 0 y 1
print(df.iloc[0:2])
```
```raw
      Nombre  Edad    Ciudad
    0    Ana    25      STGO
    1   Luis    30  Medellín
      Nombre  Edad    Ciudad
    0    Ana    25      STGO
    1   Luis    30  Medellín
```


```python showLineNumbers
# Filas y columnas específicas
print(df.loc[0:1, ['Nombre', 'Edad']])
```
```raw
      Nombre  Edad
    0    Ana    25
    1   Luis    30
```

### Eliminar filas


```python showLineNumbers
# Eliminar filas con NaN en un DataFrame:

# 1) Eliminar filas que tienen ANY NaN (no modifica el dataframe original)
df_sin_nan = df.dropna()
print("Original df shape:", df.shape, "-> sin NaN (any):", df_sin_nan.shape)

# 2) Eliminar filas que tienen NaN en columnas específicas (ej. 'Edad')
df_sin_nan_edad = df.dropna(subset=['Edad'])
print("Sin NaN en 'Edad':", df_sin_nan_edad.shape)

# 3) Eliminar filas que están completamente vacías (all NaN)
df_no_allnull = df.dropna(how='all')
print("Eliminadas filas con all NaN:", df_no_allnull.shape)

# 4) Mantener sólo filas con al menos N valores no nulos (ej. al menos 2)
df_thresh = df.dropna(thresh=2)
print("Filas con al menos 2 valores no nulos:", df_thresh.shape)

# 5) Hacer la operación in-place (modifica df)
# Atención: dropna(inplace=True) devuelve None
df_copy = df.copy()            # crear copia si no quiere perder el original
df_copy.dropna(inplace=True)
print("Copia df_copy tras dropna(inplace=True):", df_copy.shape)

# 6) Aplicado al DataFrame 'df_maximas' (eliminar filas sin temperatura)
if 'df_maximas' in globals():
    df_maximas_clean = df_maximas.dropna(subset=['Temperatura']).reset_index(drop=True)
    print("df_maximas shape:", df_maximas.shape, "-> df_maximas_clean:", df_maximas_clean.shape)
else:
    print("df_maximas no existe en el entorno actual.")
```

    Original df shape: (3, 3) -> sin NaN (any): (3, 3)
    Sin NaN en 'Edad': (3, 3)
    Eliminadas filas con all NaN: (3, 3)
    Filas con al menos 2 valores no nulos: (3, 3)
    Copia df_copy tras dropna(inplace=True): (3, 3)
    df_maximas shape: (335, 2) -> df_maximas_clean: (335, 2)


### Agregar columnas


```python showLineNumbers
#directamente
df['Departamento'] = ['Ancud', 'Antioquia', 'Ancud']
print(df)
```

      Nombre  Edad       Ciudad Departamento
    0    Ana    25         STGO        Ancud
    1   Luis    30     Medellín    Antioquia
    2  María    22  Guadalajara        Ancud



```python showLineNumbers
# Desde cálculo
df['Edad_doble'] = df['Edad'] * 2
print(df)
```

      Nombre  Edad       Ciudad Departamento  Edad_doble
    0    Ana    25         STGO        Ancud          50
    1   Luis    30     Medellín    Antioquia          60
    2  María    22  Guadalajara        Ancud          44



```python showLineNumbers
# Con condición
df['Mayor_edad'] = df['Edad'] >= 18
print(df)
```

      Nombre  Edad       Ciudad Departamento  Edad_doble  Mayor_edad
    0    Ana    25         STGO        Ancud          50        True
    1   Luis    30     Medellín    Antioquia          60        True
    2  María    22  Guadalajara        Ancud          44        True


### Eliminar columnas


```python showLineNumbers
# Eliminar columna
df_sin_dep = df.drop('Departamento', axis=1)
print(df_sin_dep)
```

      Nombre  Edad       Ciudad  Edad_doble  Mayor_edad
    0    Ana    25         STGO          50        True
    1   Luis    30     Medellín          60        True
    2  María    22  Guadalajara          44        True



```python showLineNumbers
# Eliminar fila por índice
df_sin_luis = df.drop(1)
print(df_sin_luis)
```

      Nombre  Edad       Ciudad Departamento  Edad_doble  Mayor_edad
    0    Ana    25         STGO        Ancud          50        True
    2  María    22  Guadalajara        Ancud          44        True



```python showLineNumbers
# Eliminar varias columnas
df.drop(['Edad_doble', 'Mayor_edad'], axis=1, inplace=True)
```

### Selección de datos


```python showLineNumbers
# selección con query
df.query('Edad > 25 and Ciudad == "Medellín"')
# O con variables
edad_min = 20

df.query('Edad > @edad_min')
```


### Dataframe to csv
```python showLineNumbers
import os

# Exportar el DataFrame `covid` a CSV en ../data/
data = "../data/"
os.makedirs(data, exist_ok=True)
output_path = os.path.join(data, "covid-19cases.csv")
covid.to_csv(output_path, index=False)
print(f"CSV guardado en: {output_path} ({len(covid)} filas)")
```

### Tranformar una planilla Excel en un archivo csv
Dado una planilla particular con un formato tabular pero información adicional, se requiere realizar ciertas operacione para hacerle útil para el anáisis.


```python showLineNumbers
# 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
# El problema es que al iterar por meses, el nombre 'Enero' puede tener espacios o formato diferente.
# Mejor iterar por filas y columnas, asegurando que 'Enero' se incluya correctamente.
archivo = 'https://patricioaraneda.cl/public/TemperaturaMaximaDiaria_2024.xlsx'
# Especificar el engine para archivos .xls antiguos
maximas = pd.read_excel(archivo, header=1, nrows=31, decimal=',')

if 'Dia' not in maximas.columns:
    maximas.rename(columns={maximas.columns[0]: 'Dia'}, inplace=True)
    
fechas = []
temperaturas = []

meses = maximas.columns[1:]  # Ignora la columna 'Dia'

for mes in meses:
    for idx, row in maximas.iterrows():
        dia = row['Dia']
        temp = row[mes]
        # Convertir el valor a float si es posible, reemplazando ',' por '.'
        if isinstance(temp, str):
            temp_clean = temp.replace(',', '.')
            try:
                temp_float = float(temp_clean)
            except ValueError:
                continue  # saltar si no se puede convertir
        else:
            temp_float = temp

        # Solo agregar si el valor de temperatura no es nulo y es numérico
        if pd.notnull(temp_float):
            fechas.append(f"{dia:02d}-{mes}-2024")
            temperaturas.append(temp_float)

df_maximas = pd.DataFrame({'Fecha': fechas, 'Temperatura': temperaturas})

# transforma la columna 'Fecha' en un formato de fecha en español
meses_es = {
    'Enero': 'January', 'Febrero': 'February', 'Marzo': 'March', 'Abril': 'April',
    'Mayo': 'May', 'Junio': 'June', 'Julio': 'July', 'Agosto': 'August',
    'Septiembre': 'September', 'Octubre': 'October', 'Noviembre': 'November', 'Diciembre': 'December'
}

df_maximas['Fecha'] = df_maximas['Fecha'].replace(meses_es, regex=True)
df_maximas['Fecha'] = pd.to_datetime(df_maximas['Fecha'], format='%d-%B-%Y', errors='coerce')
# formatear la columna 'Fecha' para eliminar la hora
df_maximas['Fecha'] = df_maximas['Fecha'].dt.strftime('%Y-%m-%d')

# guardar df_maximas en un archivo 'data/maximas.csv' 
# df_maximas.to_csv('../data/maximas.csv', index=False)
df_maximas.head()

```



```python showLineNumbers
#
archivo = 'https://patricioaraneda.cl/public/TemperaturaMaximaDiaria_2024.xlsx'
# Especificar el engine para archivos .xls antiguos
maximas = pd.read_excel(archivo, header=1, nrows=31)
# Renombrar la columna de los días si es necesario
if 'Dia' not in maximas.columns:
    maximas.rename(columns={maximas.columns[0]: 'Dia'}, inplace=True)

# Crear un nuevo DataFrame con columnas 'Fecha' y 'Temperatura'
fechas = []
temperaturas = []

meses = maximas.columns[1:]  # Ignora la columna 'Dia'

for mes in meses:
    for idx, row in maximas.iterrows():
        dia = row['Dia']
        temp = row[mes]
        # Solo agregar si el valor de temperatura no es nulo y es numérico
        if pd.notnull(temp) and isinstance(temp, (int, float, np.float64)):
            fechas.append(f"{dia:02d}-{mes}-2024")
            temperaturas.append(temp)

df_maximas = pd.DataFrame({'Fecha': fechas, 'Temperatura': temperaturas})

# transforma la columna 'Fecha' en un formato de fecha en español
meses_es = {
    'Enero': 'January', 'Febrero': 'February', 'Marzo': 'March', 'Abril': 'April',
    'Mayo': 'May', 'Junio': 'June', 'Julio': 'July', 'Agosto': 'August',
    'Septiembre': 'September', 'Octubre': 'October', 'Noviembre': 'November', 'Diciembre': 'December'
}

df_maximas['Fecha'] = df_maximas['Fecha'].replace(meses_es, regex=True)
df_maximas['Fecha'] = pd.to_datetime(df_maximas['Fecha'], format='%d-%B-%Y', errors='coerce')
# formatear la columna 'Fecha' para eliminar la hora
df_maximas['Fecha'] = df_maximas['Fecha'].dt.strftime('%Y-%m-%d')

# guardar df_maximas en un archivo 'data/maximas.csv' 
# df_maximas.to_csv('../data/maximas.csv', index=False)
df_maximas.head()
```




## Merge, Join
Métodos para realizar comparaciones o combinar series o dataframes, de forma similar a lo que se realiza en el entorno SQL.

Las imágenes son obtenidas de la documentación oficial de Pandas *https://pandas.pydata.org/docs/user_guide/merging.html*.

### Concatenar
Toma una lista de de objetos homogénesos y los une a lo largo de un eje realizando uniones o intersecciones lógicas entre ellos.

![](https://pandas.pydata.org/docs/_images/merging_concat_basic.png)


**NOTA**: Coleccione todas las series o dataframes en una lista antes de usar concat(). esto vitará que se puedan generar múltiples copias. Se intentará preservar los nombres de columnas incluso cuando se repitan.



```python showLineNumbers
df1 = pd.DataFrame(
        {
            "A": ["A0", "A1", "A2", "A3"],
            "B": ["B0", "B1", "B2", "B3"],
            "C": ["C0", "C1", "C2", "C3"],
         "D": ["D0", "D1", "D2", "D3"],
        },
        index=[0, 1, 2, 3],
        )

df2 = pd.DataFrame(
        {
            "A": ["A4", "A5", "A6", "A7"],
            "B": ["B4", "B5", "B6", "B7"],
            "C": ["C4", "C5", "C6", "C7"],
            "D": ["D4", "D5", "D6", "D7"],
        },
        index=[4, 5, 6, 7],
    )
    

df3 = pd.DataFrame(
        {
            "A": ["A8", "A9", "A10", "A11"],
            "B": ["B8", "B9", "B10", "B11"],
            "C": ["C8", "C9", "C10", "C11"],
            "D": ["D8", "D9", "D10", "D11"],
        },
        index=[8, 9, 10, 11],
    )
    

frames = [df1, df2, df3]

result = pd.concat(frames)

result
```



#### JOIN
Este parámetro define la forma de cómo se manejan los valores de los eje que no existan en el primer dataframe.

**join='outer'**
Establece la union de todos los ejes de valores



```python showLineNumbers
df4 = pd.DataFrame(
    {
        "B": ["B2", "B3", "B6", "B7"],
        "D": ["D2", "D3", "D6", "D7"],
        "F": ["F2", "F3", "F6", "F7"],
    },
    index=[2, 3, 6, 7],
)
result = pd.concat([df1, df4], axis=1, join='outer')
result
```




![](https://pandas.pydata.org/docs/_images/merging_concat_axis1.png)

**join='inner'**

Se suscribe a la intersección de ejes de valores.


```python showLineNumbers
result = pd.concat([df1, df4], axis=1, join='inner')
result
```



![](https://pandas.pydata.org/docs/_images/merging_concat_axis1_inner.png)

## Agregar filas a un dataframe
Para agregar una fila (serie) primero debes convertirla en dataframe y usar concat() para añadirla al dataframe destino.


```python showLineNumbers
s2 = pd.Series(["X0", "X1", "X2", "X3"], index=["A", "B", "C", "D"])
result = pd.concat([df1, s2.to_frame().T], ignore_index=True)
result
```




![](https://pandas.pydata.org/docs/_images/merging_append_series_as_row.png)

## **MERGE**

Esta función realiza operaciones de unión muy similares a las realizadas por SQL en bases de datos.
Donde se establecen uniones de tipo:
- **uno a uno**: une dos dataframes en base a sus índices que deben contener un valor único.

- **uno a muchos**: une un índice único a uno o más columnas de otro dataframe.

- **muchos a muchos**: une columnas sobre columnas.


| Método | SQL Join  | Descripción |
|---|---|---|
| left | LEFT OUTER JOIN | Usa keys del dataframe izquierdo |
| right | RIGHT OUTER JOIN | Usa keys del dataframe derecho |
| outer | FULL OUTER JOIN | Usa unión de keys de ambos dataframes |
| inner | INNER JOIN | Usa intersección de claves de ambos dataframes |
| cross | CROSS JOIN | Crea un producto cartesiano de las filas de ambos dataframes (todos por todos) |

#### INNER JOIN

En SQL:
```sql
SELECT *
FROM df1
INNER JOIN df2
  ON df1.key = df2.key;
```
En Pandas merge realiza un **inner join** por defecto:
```python showLineNumbers
pd.merge(df1, df2, on="key", join='inner')
```


#### LEFT OUTER JOIN
Muestra todos los registros desde dataframe izquierdo (df1)

En SQL:
```sql
SELECT *
FROM df1
LEFT OUTER JOIN df2
  ON df1.key = df2.key;
```
En Pandas:
```python showLineNumbers
pd.merge(df1, df2, on="key", how="left")
```


#### RIGHT JOIN
Muestra todos los registros del dataframe derecho (df2)

En SQL:
```sql
SELECT *
FROM df1
RIGHT OUTER JOIN df2
  ON df1.key = df2.key;
```
En pandas:
```python showLineNumbers
pd.merge(df1, df2, on="key", how="right")
```


#### FULL OUTER JOIN
Genera una vista de ambos dataframes independiente de si hacen match en sus indices.

En SQL:
```sql
SELECT *
FROM df1
FULL OUTER JOIN df2
  ON df1.key = df2.key;
```
En pandas:
```python showLineNumbers
pd.merge(df1, df2, on="key", how="outer")
```

---
## PIVOT Tables

![](https://pandas.pydata.org/docs/_images/reshaping_pivot.png)
