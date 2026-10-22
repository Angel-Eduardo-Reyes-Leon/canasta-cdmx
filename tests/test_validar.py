import pandas as pd

from scripts.comun import COLUMNAS_ORIGINAL
from scripts.validar import validar

PRODUCTOS = pd.DataFrame({'id_producto': ['P05', 'P09'], 'unidad_base': ['L', 'kg'],
                          'presentacion_referencia': [1.0, 1.0], 'factor_piezas_kg': [None, None]})
ESTABLECIMIENTOS = pd.DataFrame({'id_establecimiento': ['S-SUP-01', 'S-MER-01']})


def fila(**cambios):
    base = {c: '' for c in COLUMNAS_ORIGINAL}
    base.update(fecha='2026-10-24', ronda='1', hora='10:30', reprogramada='0', equipo='3', id_recolector='E3-04',
                id_establecimiento='S-SUP-01', id_producto='P05', estado='disponible', precio_etiqueta='28.5',
                cantidad_presentacion='1', unidad_presentacion='L', tipo_marca='lider', promocion='0',
                tipo_promocion='ninguna', fuente='presencial', foto='S-SUP-01-P05-R1.jpg')
    base.update(cambios)
    return base


def correr(filas):
    return validar(pd.DataFrame(filas), PRODUCTOS, ESTABLECIMIENTOS)


def test_registro_correcto():
    errores, _ = correr([fila()])
    assert errores == []


def test_detecta_repetidos():
    errores, _ = correr([fila(), fila()])
    assert any('repetido' in e for e in errores)


def test_agotado_no_lleva_precio():
    errores, _ = correr([fila(estado='agotado')])
    assert any('hay precio' in e for e in errores)


def test_precio_presencial_necesita_foto():
    errores, _ = correr([fila(foto='')])
    assert any('fotografía' in e for e in errores)


def test_codigos_fuera_de_catalogo():
    errores, _ = correr([fila(id_establecimiento='X-SUP-99'), fila(id_producto='P99')])
    assert len([e for e in errores if 'catálogo' in e]) == 2
