"""Revisa los CSV de datos/original antes de integrarlos.

Uso:
    python scripts/validar.py            revisa todas las rondas
    python scripts/validar.py --ronda 3  revisa solo la ronda 3

Termina con código 1 si hay errores. Los avisos no bloquean, pero se revisan contra la foto.
"""
import argparse
import os
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.comun import (COLUMNAS_ORIGINAL, ESTADOS, FUENTES, RAIZ, RONDAS, TIPOS_MARCA,  # noqa: E402
                           TIPOS_PROMOCION, UNIDADES, agregar_id_registro, leer_catalogos,
                           leer_originales, numeros)
from scripts.normalizar import normalizar  # noqa: E402


def validar(df, productos, establecimientos):
    """Regresa (errores, avisos) como listas de texto."""
    errores, avisos = [], []
    faltan = [c for c in COLUMNAS_ORIGINAL if c not in df.columns]
    if faltan:
        return [f'Faltan columnas: {", ".join(faltan)}'], avisos
    if df.empty:
        return errores, avisos

    df = agregar_id_registro(numeros(df))
    def lugar(i):
        return f"{df.at[i, 'archivo']} fila {i + 2}" if 'archivo' in df.columns else f'fila {i + 2}'

    for i in df.index[~df['ronda'].isin(list(RONDAS))]:
        errores.append(f'{lugar(i)}: ronda fuera de 1 a 6')
    for i in df.index[~df['id_establecimiento'].isin(establecimientos['id_establecimiento'])]:
        errores.append(f"{lugar(i)}: el establecimiento {df.at[i, 'id_establecimiento']} no está en el catálogo")
    for i in df.index[~df['id_producto'].isin(productos['id_producto'])]:
        errores.append(f"{lugar(i)}: el producto {df.at[i, 'id_producto']} no está en el catálogo")
    for i in df.index[~df['estado'].isin(ESTADOS)]:
        errores.append(f"{lugar(i)}: estado '{df.at[i, 'estado']}' no permitido")
    for i in df.index[~df['fuente'].isin(FUENTES)]:
        errores.append(f"{lugar(i)}: fuente '{df.at[i, 'fuente']}' no permitida")
    for i in df.index[~df['reprogramada'].isin([0, 1])]:
        errores.append(f'{lugar(i)}: reprogramada debe ser 0 o 1')

    repetidos = df[df.duplicated('id_registro', keep=False)]
    for reg in repetidos['id_registro'].unique():
        errores.append(f'Registro repetido: {reg}')

    disp = df['estado'] == 'disponible'
    for i in df.index[disp & ~(df['precio_etiqueta'] > 0)]:
        errores.append(f'{lugar(i)}: producto disponible sin precio válido')
    for i in df.index[~disp & df['precio_etiqueta'].notna()]:
        errores.append(f'{lugar(i)}: hay precio en una fila {df.at[i, "estado"]}')
    for i in df.index[disp & ~df['unidad_presentacion'].isin(UNIDADES)]:
        errores.append(f"{lugar(i)}: unidad '{df.at[i, 'unidad_presentacion']}' no permitida")
    for i in df.index[disp & (df['fuente'] == 'presencial') & (df['foto'].str.strip() == '')]:
        errores.append(f'{lugar(i)}: precio presencial sin fotografía')

    for i in df.index[disp & (df['tipo_marca'] != '') & ~df['tipo_marca'].isin(TIPOS_MARCA)]:
        avisos.append(f"{lugar(i)}: tipo de marca '{df.at[i, 'tipo_marca']}' no reconocido")
    for i in df.index[(df['tipo_promocion'] != '') & ~df['tipo_promocion'].isin(TIPOS_PROMOCION)]:
        avisos.append(f"{lugar(i)}: tipo de promoción '{df.at[i, 'tipo_promocion']}' no reconocido")

    norm = normalizar(df[disp], productos)
    for i in norm.index[norm['error_unidad'] != '']:
        errores.append(f"{lugar(i)}: {norm.at[i, 'error_unidad']}")

    # Precios muy lejos de la mediana del producto en la ronda: se revisan contra la foto
    ok = norm[norm['precio_normalizado'].notna()]
    mediana = ok.groupby(['id_producto', 'ronda'])['precio_normalizado'].transform('median')
    conteo = ok.groupby(['id_producto', 'ronda'])['precio_normalizado'].transform('count')
    raros = ok[(conteo >= 3) & ((ok['precio_normalizado'] < 0.5 * mediana) | (ok['precio_normalizado'] > 2 * mediana))]
    for i in raros.index:
        avisos.append(f"{lugar(i)}: {raros.at[i, 'id_registro']} tiene {raros.at[i, 'precio_normalizado']:.2f} por "
                      f"{raros.at[i, 'unidad_base']}, lejos de la mediana del producto en la ronda")

    # Presentación fuera de la mitad al doble de la de referencia
    ref = productos.set_index('id_producto')['presentacion_referencia']
    referencia = ok['id_producto'].map(ref)
    fuera = ok[(ok['contenido_base'] < 0.5 * referencia) | (ok['contenido_base'] > 2 * referencia)]
    for i in fuera.index:
        avisos.append(f"{lugar(i)}: {fuera.at[i, 'id_registro']} tiene una presentación fuera del rango permitido")
    return errores, avisos


def marcar_validos(df):
    """Un precio es válido si está disponible, es presencial, tiene foto y su precio normalizado es positivo."""
    df = df.copy()
    df['valido'] = ((df['estado'] == 'disponible') & (df['fuente'] == 'presencial')
                    & (df['foto'].str.strip() != '') & (df['precio_normalizado'] > 0)).astype(int)
    return df


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--ronda', type=int)
    parser.add_argument('--raiz', default=str(RAIZ))
    args = parser.parse_args()

    productos, establecimientos = leer_catalogos(args.raiz)
    df = leer_originales(args.raiz)
    if args.ronda:
        df = df[pd.to_numeric(df['ronda'], errors='coerce') == args.ronda].reset_index(drop=True)
    if df.empty:
        print('No hay registros en datos/original.')
        return 0

    errores, avisos = validar(df, productos, establecimientos)
    validos = 0
    if not errores:
        norm = normalizar(agregar_id_registro(numeros(df)), productos)
        validos = int(marcar_validos(norm)['valido'].sum())

    resumen = [f'Registros revisados: {len(df)}', f'Precios válidos: {validos}',
               f'Errores: {len(errores)}', f'Avisos: {len(avisos)}']
    print('\n'.join(resumen))
    for e in errores:
        print('ERROR  ' + e)
    for a in avisos:
        print('AVISO  ' + a)

    salida = os.environ.get('GITHUB_STEP_SUMMARY')
    if salida:
        with open(salida, 'a', encoding='utf-8') as f:
            f.write('## Validación de datos\n\n' + '\n'.join(f'- {r}' for r in resumen) + '\n')
    return 1 if errores else 0


if __name__ == '__main__':
    sys.exit(main())
