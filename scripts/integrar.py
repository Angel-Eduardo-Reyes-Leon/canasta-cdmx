"""Une las rondas de los cuatro equipos, aplica la bitácora y genera datos/trabajo/precios.csv.

Uso:
    python scripts/integrar.py

No modifica datos/original. Si la validación encuentra errores, no escribe nada.
"""
import argparse
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.comun import RAIZ, RONDAS_FESTIVAS, agregar_id_registro, leer_catalogos, leer_originales, numeros  # noqa: E402
from scripts.normalizar import normalizar  # noqa: E402
from scripts.validar import marcar_validos, validar  # noqa: E402

COLUMNAS_BITACORA = ['fecha', 'id_registro', 'campo', 'valor_anterior', 'valor_nuevo', 'motivo', 'responsable']


def leer_bitacora(ruta):
    """Lee la tabla de correcciones de datos/bitacora.md."""
    filas = []
    if not Path(ruta).exists():
        return pd.DataFrame(columns=COLUMNAS_BITACORA)
    for linea in Path(ruta).read_text(encoding='utf-8').splitlines():
        linea = linea.strip()
        if not linea.startswith('|') or set(linea) <= {'|', '-', ' ', ':'}:
            continue
        celdas = [c.strip() for c in linea.strip('|').split('|')]
        if celdas[:2] == ['fecha', 'id_registro']:
            continue
        if len(celdas) == len(COLUMNAS_BITACORA):
            filas.append(celdas)
    return pd.DataFrame(filas, columns=COLUMNAS_BITACORA)


def aplicar_correcciones(df, correcciones):
    """Cambia cada valor solo si el valor anterior coincide con lo que trae el archivo original."""
    df = df.copy()
    for _, c in correcciones.iterrows():
        filas = df.index[df['id_registro'] == c['id_registro']]
        if len(filas) != 1:
            raise ValueError(f"La bitácora corrige {c['id_registro']}, que no existe o está repetido")
        if c['campo'] not in df.columns:
            raise ValueError(f"La bitácora corrige el campo {c['campo']}, que no existe")
        actual = str(df.at[filas[0], c['campo']])
        if actual != c['valor_anterior']:
            raise ValueError(f"{c['id_registro']}: la bitácora espera '{c['valor_anterior']}' en {c['campo']} "
                             f"y el archivo trae '{actual}'")
        df.at[filas[0], c['campo']] = c['valor_nuevo']
    return df


def integrar(raiz=RAIZ):
    productos, establecimientos = leer_catalogos(raiz)
    df = agregar_id_registro(leer_originales(raiz))
    if df.empty:
        return df
    df = aplicar_correcciones(df, leer_bitacora(Path(raiz) / 'datos' / 'bitacora.md'))
    errores, _ = validar(df, productos, establecimientos)
    if errores:
        raise ValueError('La validación encontró errores. Corre scripts/validar.py para verlos.')

    df = marcar_validos(normalizar(numeros(df), productos))
    df['festiva'] = df['ronda'].isin(list(RONDAS_FESTIVAS)).astype(int)
    df = df.merge(productos[['id_producto', 'producto', 'grupo']], on='id_producto', how='left')
    df = df.merge(establecimientos[['id_establecimiento', 'nombre', 'tipo_comercio', 'subtipo', 'zona', 'alcaldia',
                                    'latitud', 'longitud', 'dist_transporte_m', 'equipo_responsable']],
                  on='id_establecimiento', how='left')
    return df.sort_values(['ronda', 'id_establecimiento', 'id_producto']).reset_index(drop=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--raiz', default=str(RAIZ))
    args = parser.parse_args()
    try:
        df = integrar(args.raiz)
    except ValueError as e:
        print(e)
        return 1
    if df.empty:
        print('No hay registros en datos/original.')
        return 0
    salida = Path(args.raiz) / 'datos' / 'trabajo' / 'precios.csv'
    df.drop(columns=['archivo', 'error_unidad']).to_csv(salida, index=False, encoding='utf-8')
    print(f'{len(df)} registros, {int(df["valido"].sum())} precios válidos. Archivo: {salida}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
