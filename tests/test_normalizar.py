import pandas as pd
import pytest

from scripts.normalizar import contenido_base, normalizar


def test_gramos_y_mililitros():
    assert contenido_base(900, 'ml', 'L') == pytest.approx(0.9)
    assert contenido_base(140, 'g', 'kg') == pytest.approx(0.14)
    assert contenido_base(1, 'kg', 'kg') == 1


def test_piezas_de_huevo_con_factor():
    assert contenido_base(18, 'pieza', 'kg', factor_piezas_kg=16) == pytest.approx(1.125)
    with pytest.raises(ValueError):
        contenido_base(18, 'pieza', 'kg')


def test_unidad_incompatible():
    with pytest.raises(ValueError):
        contenido_base(500, 'ml', 'kg')


def test_precio_normalizado_solo_en_disponibles():
    productos = pd.DataFrame({'id_producto': ['P06'], 'unidad_base': ['L'], 'factor_piezas_kg': [None]})
    df = pd.DataFrame({'id_producto': ['P06', 'P06'], 'estado': ['disponible', 'agotado'],
                       'precio_etiqueta': [41.5, None], 'cantidad_presentacion': [900, None],
                       'unidad_presentacion': ['ml', '']})
    res = normalizar(df, productos)
    assert res.loc[0, 'precio_normalizado'] == pytest.approx(46.1111, abs=1e-3)
    assert pd.isna(res.loc[1, 'precio_normalizado'])
