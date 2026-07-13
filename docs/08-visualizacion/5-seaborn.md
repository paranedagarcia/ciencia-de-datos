---
id: viz-seaborn
title: "Seaborn"
sidebar_label: "📊 Seaborn"
sidebar_position: 5
---

![](img/seaborn.svg)


Seaborn es una biblioteca de visualización de datos en Python basada en Matplotlib. Proporciona una interfaz de alto nivel para crear gráficos estadísticos atractivos y fáciles de interpretar. Seaborn está diseñado para trabajar bien con estructuras de datos como DataFrames de pandas, lo que facilita la creación de gráficos complejos con pocas líneas de código.

### Anatomía de un gráfico

![](https://github.com/paranedagarcia/Cienciadedatos/blob/main/images/plt.anatomia.png?raw=true)

## Instalación
Para instalar Seaborn, puedes usar pip. Abre tu terminal o línea de comandos y ejecuta el siguiente comando:
```bash
pip install seaborn
ó
uv add seaborn
```
## Importación
Para comenzar a usar Seaborn en tu proyecto de Python, primero debes importarlo. También es común importar Matplotlib para personalizar los gráficos si es necesario:
```python
import seaborn as sns
import matplotlib.pyplot as plt
```
## Ejemplo básico
Aquí tienes un ejemplo básico de cómo crear un gráfico de dispersión utilizando Seaborn:


```python
import seaborn as sns
import matplotlib.pyplot as plt
import requests
import pandas as pd
from io import StringIO
import urllib3

# Suppress insecure request warnings when using verify=False below (only for local/example use).
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Cargar un conjunto de datos de ejemplo desde el repositorio de seaborn usando requests
# Usamos verify=False para evitar el error de validación SSL en entornos locales.
url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv"
resp = requests.get(url, verify=False)
resp.raise_for_status()
tips = pd.read_csv(StringIO(resp.text))

# Crear un gráfico de dispersión
plt.figure(figsize=(10, 6))
sns.scatterplot(data=tips, x="total_bill", y="tip", hue="day")
plt.title("Gráfico de dispersión de propinas")
plt.show()
```
![](img/4-seaborn-propinas.png)

En este ejemplo, cargamos un conjunto de datos de ejemplo llamado "tips" y creamos un gráfico de dispersión que muestra la relación entre la cuenta total y la propina, diferenciando los puntos por día de la semana.
## Documentación oficial
Para obtener más información sobre Seaborn y explorar todas sus funcionalidades, puedes visitar la [documentación oficial de Seaborn](https://seaborn.pydata.org/).




```python
sns.displot( data=tips, x='total_bill', kind='kde', hue='sex' )
```

    
![png](img/4-seaborn_4_1.png)
    


# Análisis exploratorio (EDA) — Titanic

Objetivo: 
explorar la estructura, distribuciones, relaciones y valores perdidos del archivo '../data/titanic5_full.csv' usando únicamente gráficos de seaborn. A continuación se presentan los pasos recomendados y fragmentos de código listos para ejecutar en celdas de código (no repetir imports ya presentes).

Carga y resumen inicial



```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('../data/titanic5_price_clean.csv')
df.head()
df.info()
df.describe(include='all')
```
```raw
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 2208 entries, 0 to 2207
    Data columns (total 18 columns):
     #   Column       Non-Null Count  Dtype  
    ---  ------       --------------  -----  
     0   Sex          2208 non-null   int64  
     1   Age          2154 non-null   float64
     2   Class/Dept   2208 non-null   object 
     3   Class        2208 non-null   object 
     4   Ticket       1317 non-null   object 
     5   Joined       2208 non-null   object 
     6   Occupation   1587 non-null   object 
     7   Boat [Body]  2208 non-null   object 
     8   Price        2208 non-null   float64
     9   Job          958 non-null    object 
     10  Survived     2208 non-null   int64  
     11  Title        2208 non-null   object 
     12  DoB          1231 non-null   object 
     13  Year_Birth   621 non-null    object 
     14  Date_Death   2087 non-null   object 
     15  DoB_Clean    1853 non-null   object 
     16  sibsp        1309 non-null   float64
     17  parch        1309 non-null   float64
    dtypes: float64(4), int64(2), object(12)
    memory usage: 310.6+ KB
```




```python
# Configuración estética (opcional)
sns.set_theme(style='whitegrid', palette='deep')
```

### Gráficos recomendados

**1) Mapa de valores faltantes**


```python
plt.figure(figsize=(10,4))
sns.heatmap(df.isnull(), cbar=False, yticklabels=False, cmap='viridis')
plt.title('Valores faltantes')
plt.show()
```


![png](img/4-seaborn_9_0.png)
    

```python

plt.figure(figsize=(12,4))
plt.subplot(1,3,1)
sns.histplot(df['Age'].dropna(), kde=True)
plt.title('Distribución de Age')

plt.subplot(1,3,2)
sns.histplot(df['Class'].dropna(), kde=True)
plt.title('Distribución de Class')

plt.subplot(1,3,3)
sns.histplot(df['sibsp'].dropna(), kde=False, bins=8)
plt.title('Distribución de SibSp')
plt.tight_layout()
plt.show()
```

    
![png](img/4-seaborn_11_0.png)
    



3) Boxplots 
- violines para detectar outliers y comparar por grupo


```python

plt.figure(figsize=(10,4))
plt.subplot(1,2,1)
sel_df = df[df['Class'].astype(str).isin(['1','2','3'])]
sns.boxplot(x='Class', y='Price', data=sel_df)
plt.title('Price por Class')

plt.subplot(1,2,2)
sns.violinplot(x='Survived', y='Age', data=df, hue='Survived', split=False)
plt.title('Age por Survived')
plt.tight_layout()
plt.show()

```


    
![png](img/4-seaborn_13_0.png)
    



4) Conteos de variables categóricas
- survived, sex, pclass, embarked



```python

plt.figure(figsize=(12,8))
plt.subplot(2,2,1)
sns.countplot(x='Survived', data=df)
plt.title('Conteo Survived')

plt.subplot(2,2,2)
sns.countplot(x='Sex', data=df)
plt.title('Conteo Sex')

plt.subplot(2,2,3)
sns.countplot(x='Class', data=df)
plt.title('Conteo Class')

plt.subplot(2,2,4)
sns.countplot(x='Joined', data=df)
plt.title('Conteo Joined')
plt.tight_layout()
plt.show()

```


    
![png](img/4-seaborn_15_0.png)
    


5) Tasa de supervivencia por categoría (barplot con mean)


```python
plt.figure(figsize=(12,4))
plt.subplot(1,3,1)
sns.barplot(x='Class', y='Survived', data=df, errorbar=None)
plt.title('Survival rate por Pclass')

plt.subplot(1,3,2)
sns.barplot(x='Sex', y='Survived', data=df, errorbar=None)
plt.title('Survival rate por Sex')

plt.subplot(1,3,3)
sns.barplot(x='Joined', y='Survived', data=df, errorbar=None)
plt.title('Survival rate por Embarked')
# rota 45 grados xlabels
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```
    
![png](img/4-seaborn_17_1.png)
    



6) Interacciones categóricas (FacetGrid / catplot)
- Survival por Class y Sex


```python
plt.figure(figsize=(10,6))
sns.catplot(x='Class', y='Survived', hue='Sex', kind='point', data=df, ci=None, height=4, aspect=1.5)
plt.title('Survival rate por Class y Sex')
plt.show()

```

![png](img/4-seaborn_19_2.png)
    


7) Relaciones numéricas bivariadas
- Age vs Fare coloreado por Survived



```python

plt.figure(figsize=(10,6))
sns.scatterplot(data=df, x='Age', y='Price', hue='Survived', alpha=0.7)
plt.title('Age vs Price (colored by Survived)')
plt.show()

```


    
![png](img/4-seaborn_21_0.png)
    



- Si hay muchos puntos, usar kdeplot o hexbin-style con jointplot



```python
# define tamaño de figura a 10,6
plt.figure(figsize=(10,6))

sns.jointplot(data=df, x='Age', y='Price', kind='kde', hue='Survived')
plt.show()

```


    
![png](img/4-seaborn_23_1.png)
    




8) Matriz de correlación (numéricas) y heatmap



```python
num = df.select_dtypes(include=['int64','float64'])
corr = num.corr()
plt.figure(figsize=(10,6))
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Correlación entre variables numéricas')
plt.show()
```


    
![png](img/4-seaborn_25_0.png)
    




9) Pairplot para ver relaciones múltiples (filtrar columnas si hay muchas)



```python

cols = ['Survived','Age','Price','sibsp','parch']
sns.pairplot(df[cols].dropna(), hue='Survived', diag_kind='kde', corner=True)
plt.show()

```


    
![png](img/4-seaborn_27_0.png)
    




10) Análisis de títulos / familias si existen (feature engineering)
- Si hay columna name: extraer título y visualizar survival por título (ejemplo)


```python
# ejemplo de ingeniería si aplica
#df['title'] = df['name'].str.extract(',\s*([^\.]+)\.')
plt.figure(figsize=(10,6))
sns.countplot(y='Title', hue='Survived', data=df, order=df['Title'].value_counts().index)
plt.title('Survival por Title')
plt.show()
```


    
![png](img/4-seaborn_29_0.png)
    




11) Análisis de tamaño familiar (SibSp + Parch)



```python

df['family_size'] = df.get('sibsp', df.get('sibsp', 0)) + df.get('parch', df.get('parch', 0)) + 1
plt.figure(figsize=(10,6))
sns.countplot(x='family_size', hue='Survived', data=df)
plt.title('Survival por tamaño de familia')
plt.show()

```


    
![png](img/4-seaborn_31_0.png)
    

