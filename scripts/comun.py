"""Rutas, catálogos y valores permitidos que comparten los scripts."""
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[1]

RONDAS = range(1, 7)
RONDAS_FESTIVAS = {2: 'Día de Muertos', 4: 'El Buen Fin'}

ESTADOS = {'disponible', 'agotado', 'no_manejado', 'no_visitado'}
UNIDADES = {'g', 'kg', 'ml', 'L', 'pieza'}
FUENTES = {'presencial', 'en_linea'}
TIPOS_MARCA = {'lider', 'propia', 'generica', 'granel'}
TIPOS_PROMOCION = {'ninguna', 'directa', '2x1', '3x2', 'multiple', 'tarjeta'}

COLUMNAS_ORIGINAL = [
    'fecha', 'ronda', 'hora', 'reprogramada', 'equipo', 'id_recolector', 'id_establecimiento',
    'id_puesto', 'id_producto', 'estado', 'precio_etiqueta', 'cantidad_presentacion',
    'unidad_presentacion', 'marca', 'tipo_marca', 'promocion', 'tipo_promocion',
    'condicion_promocion', 'precio_regular', 'fuente', 'foto', 'observaciones',
]
NUMERICAS = ['ronda', 'reprogramada', 'equipo', 'precio_etiqueta', 'cantidad_presentacion', 'promocion', 'precio_regular']


def leer_csv(ruta):
    return pd.read_csv(ruta, dtype=str, keep_default_na=False, encoding='utf-8')


def leer_catalogos(raiz=RAIZ):
    cat = Path(raiz) / 'datos' / 'catalogos'
    productos = leer_csv(cat / 'productos.csv')
    for c in ['presentacion_referencia', 'cantidad_semanal', 'factor_piezas_kg', 'activo']:
        productos[c] = pd.to_numeric(productos[c], errors='coerce')
    establecimientos = leer_csv(cat / 'establecimientos.csv')
    for c in ['latitud', 'longitud', 'dist_transporte_m', 'dist_referencia_km', 'equipo_responsable']:
        establecimientos[c] = pd.to_numeric(establecimientos[c], errors='coerce')
    return productos, establecimientos


def leer_originales(raiz=RAIZ):
    """Une todos los CSV de datos/original y guarda de qué archivo salió cada fila."""
    archivos = sorted((Path(raiz) / 'datos' / 'original').glob('*.csv'))
    if not archivos:
        return pd.DataFrame(columns=COLUMNAS_ORIGINAL + ['archivo'])
    partes = []
    for a in archivos:
        df = leer_csv(a)
        df['archivo'] = a.name
        partes.append(df)
    return pd.concat(partes, ignore_index=True)


def numeros(df):
    df = df.copy()
    for c in NUMERICAS:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c].replace('', None), errors='coerce')
    return df


def agregar_id_registro(df):
    df = df.copy()
    ronda = pd.to_numeric(df['ronda'], errors='coerce').astype('Int64').astype(str)
    df['id_registro'] = df['id_establecimiento'] + '-' + df['id_producto'] + '-R' + ronda
    return df
