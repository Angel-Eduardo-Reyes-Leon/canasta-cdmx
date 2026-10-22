"""Convierte cada precio a precio por kilo, litro o pieza."""
import numpy as np
import pandas as pd

FACTORES = {('g', 'kg'): 0.001, ('kg', 'kg'): 1.0, ('ml', 'L'): 0.001, ('L', 'L'): 1.0}


def contenido_base(cantidad, unidad, unidad_base, factor_piezas_kg=None):
    """Cantidad del envase expresada en la unidad base del producto."""
    if cantidad is None or not cantidad > 0:
        raise ValueError('La cantidad de la presentación debe ser mayor que cero')
    if unidad == 'pieza':
        if unidad_base == 'pieza':
            return float(cantidad)
        if factor_piezas_kg and factor_piezas_kg > 0:
            return float(cantidad) / float(factor_piezas_kg)
        raise ValueError('Falta el factor de piezas por kilo para convertir piezas a kg')
    if (unidad, unidad_base) not in FACTORES:
        raise ValueError(f'La unidad {unidad} no se puede convertir a {unidad_base}')
    return float(cantidad) * FACTORES[(unidad, unidad_base)]


def normalizar(df, productos):
    """Agrega contenido_base, unidad_base y precio_normalizado a las filas disponibles."""
    cat = productos.set_index('id_producto')
    df = df.copy()
    df['unidad_base'] = df['id_producto'].map(cat['unidad_base'])
    contenidos, errores = [], []
    for _, fila in df.iterrows():
        if fila.get('estado') != 'disponible':
            contenidos.append(np.nan)
            errores.append('')
            continue
        try:
            factor = cat.at[fila['id_producto'], 'factor_piezas_kg'] if fila['id_producto'] in cat.index else None
            contenidos.append(contenido_base(fila['cantidad_presentacion'], fila['unidad_presentacion'],
                                             fila['unidad_base'], factor))
            errores.append('')
        except (ValueError, TypeError, KeyError) as e:
            contenidos.append(np.nan)
            errores.append(str(e))
    df['contenido_base'] = contenidos
    df['error_unidad'] = errores
    df['precio_normalizado'] = (pd.to_numeric(df['precio_etiqueta'], errors='coerce') / df['contenido_base']).round(4)
    return df
