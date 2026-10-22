"""Reporte semanal de precios válidos por equipo, zona, alcaldía, tipo de comercio y ronda.

Uso:
    python scripts/cobertura.py

Lee datos/trabajo/precios.csv y escribe reportes/cobertura/cobertura_ronda_XX.md.
"""
import argparse
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.comun import RAIZ  # noqa: E402

META_POR_RONDA = 500
META_EQUIPO = {1: 800, 2: 734, 3: 734, 4: 734}
CONTROLES = {3: 1500, 5: 2500, 6: 3000}


def tabla_md(df):
    columnas = list(df.columns)
    lineas = ['| ' + ' | '.join(map(str, columnas)) + ' |', '|' + '---|' * len(columnas)]
    lineas += ['| ' + ' | '.join(str(v) for v in fila) + ' |' for fila in df.itertuples(index=False)]
    return '\n'.join(lineas)


def reporte(df):
    ultima = int(df['ronda'].max())
    validos = df[df['valido'] == 1]

    por_ronda = (validos.groupby('ronda').size().reindex(range(1, ultima + 1), fill_value=0)
                 .rename('validos').reset_index())
    por_ronda['acumulado'] = por_ronda['validos'].cumsum()
    por_ronda['meta_acumulada'] = por_ronda['ronda'] * META_POR_RONDA

    por_equipo = validos.groupby('equipo').size().rename('validos').reset_index()
    por_equipo['meta_a_la_fecha'] = por_equipo['equipo'].map(META_EQUIPO).mul(ultima / 6).round().astype(int)
    por_equipo['programados'] = por_equipo['equipo'].map(df.groupby('equipo').size())

    secciones = [f'# Cobertura al cierre de la ronda {ultima}', '',
                 f'Precios válidos acumulados: {len(validos)} de {len(df)} registros.', '']
    if ultima in CONTROLES:
        estado = 'se cumple' if len(validos) >= CONTROLES[ultima] else 'no se cumple'
        secciones += [f'Punto de control de la ronda {ultima}: mínimo {CONTROLES[ultima]}, {estado}.', '']
    secciones += ['## Por ronda', '', tabla_md(por_ronda), '', '## Por equipo', '', tabla_md(por_equipo), '']
    for col, titulo in [('zona', 'Por zona'), ('alcaldia', 'Por alcaldía'), ('tipo_comercio', 'Por tipo de comercio')]:
        t = pd.DataFrame({'registros': df.groupby(col).size(), 'validos': validos.groupby(col).size()}).fillna(0)
        t['cobertura_%'] = (100 * t['validos'] / t['registros']).round(1)
        secciones += [f'## {titulo}', '', tabla_md(t.astype({'validos': int}).reset_index()), '']
    return ultima, '\n'.join(secciones)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--raiz', default=str(RAIZ))
    args = parser.parse_args()
    ruta = Path(args.raiz) / 'datos' / 'trabajo' / 'precios.csv'
    if not ruta.exists():
        print('Primero corre scripts/integrar.py')
        return 1
    df = pd.read_csv(ruta)
    ultima, texto = reporte(df)
    salida = Path(args.raiz) / 'reportes' / 'cobertura' / f'cobertura_ronda_{ultima:02d}.md'
    salida.write_text(texto, encoding='utf-8')
    print(texto)
    return 0


if __name__ == '__main__':
    sys.exit(main())
