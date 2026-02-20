import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

CARPETA = r"c:\Users\adrig\Documents\ejercicio"

archivos = [
    "Historico_IV.xlsx",
    "Historico_PM10.xlsx",
    "Historico_IntervencionesIDU.xls",
    "Historico_UMV.xlsx",
]

def analizar_archivo(nombre):
    ruta = os.path.join(CARPETA, nombre)
    tamano = os.path.getsize(ruta)

    print(f"\n{'='*80}")
    print(f"  ARCHIVO: {nombre}")
    print(f"  Tamaño: {tamano/1024:.1f} KB")
    print(f"{'='*80}")

    if nombre.endswith('.xls'):
        df = pd.read_excel(ruta, engine='xlrd')
    else:
        df = pd.read_excel(ruta, engine='openpyxl')

    # 1. Informacion basica
    print(f"\n--- 1. INFORMACION BASICA ---")
    print(f"Filas: {df.shape[0]}")
    print(f"Columnas: {df.shape[1]}")
    print(f"\nNombres de columnas:")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i}. {col}")

    # 2. Tipos de datos y nulos
    print(f"\n--- 2. TIPOS DE DATOS Y VALORES NULOS ---")
    print(f"{'Columna':<40} {'Tipo pandas':<20} {'Tipo general':<15} {'Nulos':<8} {'% Nulos':<8}")
    print("-" * 91)
    for col in df.columns:
        dtype = str(df[col].dtype)
        nulos = df[col].isnull().sum()
        pct = (nulos / len(df)) * 100 if len(df) > 0 else 0

        if 'int' in dtype or 'float' in dtype:
            tipo_gen = 'Numerico'
        elif 'datetime' in dtype:
            tipo_gen = 'Fecha'
        elif 'object' in dtype:
            # Intentar detectar fechas en columnas object
            muestra = df[col].dropna().head(20)
            try:
                pd.to_datetime(muestra)
                tipo_gen = 'Fecha (texto)'
            except:
                tipo_gen = 'Texto'
        else:
            tipo_gen = dtype

        print(f"  {str(col):<38} {dtype:<20} {tipo_gen:<15} {nulos:<8} {pct:.1f}%")

    # 3. Estadisticas descriptivas
    print(f"\n--- 3. ESTADISTICAS DESCRIPTIVAS ---")

    # Numericas
    num_cols = df.select_dtypes(include=['int64', 'int32', 'float64', 'float32']).columns
    if len(num_cols) > 0:
        print(f"\n  [Columnas Numericas]")
        for col in num_cols:
            serie = df[col].dropna()
            if len(serie) == 0:
                print(f"  {col}: Sin datos validos")
                continue
            print(f"\n  >> {col}")
            print(f"     Min: {serie.min():.4f}")
            print(f"     Max: {serie.max():.4f}")
            print(f"     Media: {serie.mean():.4f}")
            print(f"     Mediana: {serie.median():.4f}")
            print(f"     Desv. Estandar: {serie.std():.4f}")
            print(f"     Datos validos: {len(serie)}")

    # Texto
    text_cols = df.select_dtypes(include=['object']).columns
    if len(text_cols) > 0:
        print(f"\n  [Columnas de Texto]")
        for col in text_cols:
            serie = df[col].dropna()
            n_unicos = serie.nunique()
            print(f"\n  >> {col}")
            print(f"     Valores unicos: {n_unicos}")
            if n_unicos <= 30:
                freqs = serie.value_counts().head(10)
                print(f"     Top valores:")
                for val, cnt in freqs.items():
                    print(f"       - '{val}': {cnt} ({cnt/len(df)*100:.1f}%)")
            else:
                freqs = serie.value_counts().head(5)
                print(f"     Top 5 valores:")
                for val, cnt in freqs.items():
                    print(f"       - '{val}': {cnt} ({cnt/len(df)*100:.1f}%)")

    # Fechas
    date_cols = df.select_dtypes(include=['datetime64']).columns
    if len(date_cols) > 0:
        print(f"\n  [Columnas de Fecha]")
        for col in date_cols:
            serie = df[col].dropna()
            print(f"\n  >> {col}")
            print(f"     Fecha minima: {serie.min()}")
            print(f"     Fecha maxima: {serie.max()}")
            print(f"     Rango: {(serie.max() - serie.min()).days} dias")

    # Primeras filas
    print(f"\n--- PRIMERAS 5 FILAS ---")
    print(df.head().to_string())

    print(f"\n--- ULTIMAS 3 FILAS ---")
    print(df.tail(3).to_string())

    return df

# Ejecutar analisis
dataframes = {}
for archivo in archivos:
    try:
        dataframes[archivo] = analizar_archivo(archivo)
    except Exception as e:
        print(f"\nERROR al leer {archivo}: {e}")

# Resumen comparativo
print(f"\n\n{'='*80}")
print(f"  RESUMEN COMPARATIVO")
print(f"{'='*80}")
print(f"\n{'Archivo':<40} {'Filas':<10} {'Columnas':<10}")
print("-" * 60)
for nombre, df in dataframes.items():
    print(f"  {nombre:<38} {df.shape[0]:<10} {df.shape[1]:<10}")

# Buscar columnas en comun
print(f"\n--- COLUMNAS EN COMUN ---")
all_cols = {}
for nombre, df in dataframes.items():
    for col in df.columns:
        col_lower = str(col).lower().strip()
        if col_lower not in all_cols:
            all_cols[col_lower] = []
        all_cols[col_lower].append(nombre)

for col, archivos_col in all_cols.items():
    if len(archivos_col) > 1:
        print(f"  '{col}' aparece en: {', '.join(archivos_col)}")
