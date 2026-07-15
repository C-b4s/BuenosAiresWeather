import os
import sys
import subprocess
from pathlib import Path
from functools import reduce
from typing import Callable, Tuple
import pandas as pd

RUTA_ARCHIVO = "tabulados_seguridad.csv"
ARCHIVO_SALIDA = "datos_limpios.csv"
DELIMITADOR = ","
CHUNK_SIZE = 50000

LIMITES_NUMERICOS = {
    'inferior': 0.0,
    'superior': 1000000.0
}

VALORES_CENTINELA = [
    "-1", "NaN", "NA", "n/a", "999", "9999", "999999", "N/A", "-", "---", "null", "vacío", "*", "s/n"
]

COLUMNAS_NECESARIAS = None


def compose(*functions: Callable) -> Callable:
    """Compone una secuencia de funciones puras."""
    return reduce(lambda f, g: lambda x: g(f(x)), functions)


def crear_pipeline_procesamiento(limites: dict) -> Callable:
    """
    Crea y retorna un pipeline de funciones puras mediante composición.
    Las funciones de limpieza se implementan como funciones anidadas para 
    evitar polución del namespace global, ya que solo tienen utilidad dentro de este pipeline.
    """
    def normalizar_columnas(df: pd.DataFrame) -> pd.DataFrame:
        df_norm = df.copy()
        df_norm.columns = (
            df_norm.columns.astype(str)
            .str.strip()
            .str.lower()
            .str.replace(r'[^a-záéíóúñü0-9_]', '_', regex=True)
            .str.replace(r'_+', '_', regex=True)
            .str.strip('_')
        )
        return df_norm

    def eliminar_filas_vacias(df: pd.DataFrame) -> pd.DataFrame:
        return df.dropna(how='all')

    def eliminar_duplicados_df(df: pd.DataFrame) -> pd.DataFrame:
        return df.drop_duplicates()

    def tratar_nulos(df: pd.DataFrame) -> pd.DataFrame:
        df_tratado = df.copy()
        cols_num = df_tratado.select_dtypes(include=['number']).columns
        cols_cat = df_tratado.select_dtypes(exclude=['number']).columns
        
        for col in df_tratado.columns:
            if df_tratado[col].isna().any():
                if col in cols_num:
                    mediana = df_tratado[col].median()
                    valor_imputacion = mediana if pd.notnull(mediana) else 0.0
                    df_tratado[col] = df_tratado[col].fillna(valor_imputacion)
                elif col in cols_cat:
                    df_tratado[col] = df_tratado[col].fillna('SIN_DATO')
        return df_tratado

    def estandarizar_textos(df: pd.DataFrame) -> pd.DataFrame:
        df_limpio = df.copy()
        cols_texto = df_limpio.select_dtypes(include=['object', 'string']).columns
        for col in cols_texto:
            df_limpio[col] = df_limpio[col].apply(
                lambda x: str(x).strip().upper() if pd.notnull(x) and isinstance(x, str) else x
            )
        return df_limpio

    def convertir_tipos(df: pd.DataFrame) -> pd.DataFrame:
        df_conv = df.copy()
        for col in df_conv.columns:
            try:
                df_conv[col] = pd.to_numeric(df_conv[col])
            except (ValueError, TypeError):
                pass
        return df_conv

    def limitar_valores_extremos(df: pd.DataFrame) -> pd.DataFrame:
        df_tratado = df.copy()
        cols_num = df_tratado.select_dtypes(include=['number']).columns
        for col in cols_num:
            df_tratado[col] = df_tratado[col].clip(
                lower=limites.get('inferior'),
                upper=limites.get('superior')
            )
        return df_tratado

    return compose(
        normalizar_columnas,
        eliminar_filas_vacias,
        eliminar_duplicados_df,
        tratar_nulos,
        estandarizar_textos,
        convertir_tipos,
        limitar_valores_extremos
    )


def calcular_estadisticas(df_original: pd.DataFrame, df_procesado: pd.DataFrame) -> Tuple[pd.Series, int, int]:
    """
    Función pura para calcular estadísticas.
    Retorna métricas inmutables sin modificar ninguna variable externa.
    """
    nulos = df_original.isna().sum()
    total_inicial = len(df_original)
    sin_vacias = df_original.dropna(how='all')
    vacias = total_inicial - len(sin_vacias)
    duplicados = len(sin_vacias) - len(df_procesado)
    return nulos, vacias, duplicados


def sumar_series(s1: pd.Series, s2: pd.Series) -> pd.Series:
    """Suma dos Series de pandas de manera pura, retornando una nueva Serie."""
    if s1.empty:
        return s2.copy()
    return s1.add(s2, fill_value=0)


def validar_archivo(ruta: Path) -> None:
    if not ruta.exists():
        raise FileNotFoundError(f"El archivo no existe: {ruta}")
    if not ruta.is_file():
        raise IsADirectoryError(f"La ruta no es un archivo, sino un directorio: {ruta}")
    if ruta.suffix.lower() != '.csv':
        raise ValueError(f"Extensión incorrecta. Se requiere .csv: {ruta}")
    if not os.access(ruta, os.R_OK):
        raise PermissionError(f"Sin permisos de lectura: {ruta}")

    
def sanity_checks(ruta: Path, delimitador: str) -> None:
    script_comprobacion = f"""
import sys
try:
    total = 0
    min_len = float('inf')
    max_len = 0
    min_delim = float('inf')
    max_delim = 0
    
    with open(r'{ruta.resolve()}', 'r', encoding='utf-8', errors='ignore') as f:
        for linea in f:
            total += 1
            l_len = len(linea)
            if l_len < min_len: min_len = l_len
            if l_len > max_len: max_len = l_len
            
            d_count = linea.count('{delimitador}')
            if d_count < min_delim: min_delim = d_count
            if d_count > max_delim: max_delim = d_count
            
    if total == 0:
        print("0|0-0|0-0|No")
        sys.exit(0)
        
    diff_cols = min_delim != max_delim
    print(f"{{total}}|{{min_len}}-{{max_len}}|{{min_delim}}-{{max_delim}}|{{'Sí' if diff_cols else 'No'}}")
except Exception as e:
    print(f"ERROR|{{str(e)}}")
"""
    try:
        resultado = subprocess.run(
            [sys.executable, "-c", script_comprobacion],
            capture_output=True,
            text=True,
            check=True
        )
        salida = resultado.stdout.strip().split('|')
        
        if len(salida) == 2 and salida[0] == "ERROR":
            raise RuntimeError(f"Error en sanity checks: {salida[1]}")
            
        if len(salida) == 4:
            print("--- Resultados de Sanity Checks ---")
            print(f"Número total de líneas: {salida[0]}")
            print(f"Longitud de líneas (min - max): {salida[1]}")
            print(f"Cantidad de delimitadores por línea (min - max): {salida[2]}")
            print(f"Detección de líneas con número diferente de columnas: {salida[3]}")
            print("-----------------------------------")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Fallo en subprocess para sanity checks: {e}")

def detectar_codificacion(ruta: Path, delimitador: str) -> str:
    for cod in ["utf-8", "utf-8-sig", "latin-1", "iso-8859-1"]:
        try:
            pd.read_csv(ruta, encoding=cod, sep=delimitador, nrows=5)
            return cod
        except (UnicodeDecodeError, pd.errors.ParserError):
            continue
    return "utf-8"

def imprimir_resultados(conteo_nulos: pd.Series, total_registros_iniciales: int, 
                        total_registros_procesados: int, total_vacias_eliminadas: int, 
                        total_duplicados_eliminados: int, archivo_salida: str) -> None:
    print("\n--- Conteo de Valores Nulos por Columna (Previo a Limpieza) ---")
    for col, nulos in conteo_nulos.items():
        porcentaje = (nulos / total_registros_iniciales * 100) if total_registros_iniciales > 0 else 0
        print(f"{col}: {int(nulos)} nulos ({porcentaje:.2f}%)")
        
    total_eliminados = total_vacias_eliminadas + total_duplicados_eliminados
    
    print("\n--- Resumen de Ejecución ---")
    print(f"Registros procesados exitosamente: {total_registros_procesados}")
    print(f"Total de registros eliminados: {total_eliminados}")
    print(f"  - Filas completamente vacías eliminadas: {total_vacias_eliminadas}")
    print(f"  - Registros duplicados eliminados: {total_duplicados_eliminados}")
    print(f"Nombre del archivo generado: {archivo_salida}")
    print("\nProcesado correctamente.")


def procesar_archivo(ruta_str: str, salida_str: str) -> None:
    """Maneja la lógica de Entrada y Salida (I/O) exclusivamente."""
    ruta = Path(ruta_str)
    validar_archivo(ruta)
    sanity_checks(ruta, DELIMITADOR)
    codificacion = detectar_codificacion(ruta, DELIMITADOR)
    
    columnas_disponibles = pd.read_csv(ruta, encoding=codificacion, sep=DELIMITADOR, nrows=0).columns
    usecols = COLUMNAS_NECESARIAS if COLUMNAS_NECESARIAS and all(c in columnas_disponibles for c in COLUMNAS_NECESARIAS) else None
    
    iterador_csv = pd.read_csv(
        ruta,
        encoding=codificacion,
        sep=DELIMITADOR,
        na_values=VALORES_CENTINELA,
        usecols=usecols,
        chunksize=CHUNK_SIZE,
        on_bad_lines='skip',
        low_memory=False
    )

    pipeline_funcional = crear_pipeline_procesamiento(LIMITES_NUMERICOS)
    total_registros_procesados = 0
    total_registros_iniciales = 0
    total_vacias_eliminadas = 0
    total_duplicados_eliminados = 0
    conteo_nulos = pd.Series(dtype=int)

    for i, chunk in enumerate(iterador_csv):
        primer_chunk = (i == 0)
        chunk_procesado = pipeline_funcional(chunk)
        nulos_chunk, vacias, duplicados = calcular_estadisticas(chunk, chunk_procesado)
        conteo_nulos = sumar_series(conteo_nulos, nulos_chunk)
        total_registros_iniciales += len(chunk)
        total_registros_procesados += len(chunk_procesado)
        total_vacias_eliminadas += vacias
        total_duplicados_eliminados += duplicados
        modo_escritura = 'w' if primer_chunk else 'a'
        chunk_procesado.to_csv(
            salida_str,
            mode=modo_escritura,
            header=primer_chunk,
            index=False,
            encoding='utf-8-sig',
            sep=DELIMITADOR
        )

    imprimir_resultados(
        conteo_nulos,
        total_registros_iniciales,
        total_registros_procesados,
        total_vacias_eliminadas,
        total_duplicados_eliminados,
        salida_str
    )


def main():
    try:
        procesar_archivo(RUTA_ARCHIVO, ARCHIVO_SALIDA)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()
