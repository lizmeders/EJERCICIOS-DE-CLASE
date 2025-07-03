# Importamos la librería pandas para manejar los datos
import pandas as pd

# Ruta absoluta donde está ubicado nuestro archivo CSV
ruta_archivo = r'C:\Users\lizme\Desktop\BIT\BOOTCAMP CIENCIA DE DATOS\EJERCICIOS-DE-CLASE\Clases\Clase 12_ Visualización de datos en Python\ACTIVIDAD DE DASH\CAPACIAD_INSTALADA.csv'

# Cargamos el archivo CSV en un DataFrame, con low_memory=False para evitar advertencias
df = pd.read_csv(ruta_archivo, low_memory=False)

# Mostramos la cantidad de valores nulos que tiene cada columna
print("Valores nulos por columna:")
print(df.isnull().sum())

# Eliminamos filas con valores faltantes en columnas importantes para el análisis
df = df.dropna(subset=['Gerente', 'Dirección', 'Email', 'Teléfono'])

# Convertimos la columna 'num cantidad capacidad instalada' a numérica,
# forzando a NaN aquellos valores que no se puedan convertir correctamente
df['num cantidad capacidad instalada'] = pd.to_numeric(df['num cantidad capacidad instalada'], errors='coerce')

# Revisamos cuántos valores se volvieron NaN tras convertir la columna
print("\nValores convertidos a NaN tras corregir tipos:")
print(df['num cantidad capacidad instalada'].isnull().sum())

# Eliminamos las filas que quedaron con NaN en 'num cantidad capacidad instalada' después de la conversión
df = df.dropna(subset=['num cantidad capacidad instalada'])

# Eliminamos columnas que no aportan información relevante o que tienen un único valor constante
# ('Fuente' y 'Fecha Corte' no varían y no aportan al análisis)
df = df.drop(columns=['Fuente', 'Fecha Corte'])

# Mostramos la información final del DataFrame ya limpio y listo para análisis
print("\nInformación tras limpieza:")
print(df.info())

# Guardamos el DataFrame limpio en un nuevo archivo CSV
df.to_csv(r'C:\Users\lizme\Desktop\BIT\BOOTCAMP CIENCIA DE DATOS\EJERCICIOS-DE-CLASE\Clases\Clase 12_ Visualización de datos en Python\ACTIVIDAD DE DASH\CAPACIDAD_INSTALADA_LIMPIA.csv', index=False)

print("✅ Archivo limpio guardado exitosamente.")