# Canasta CDMX

Comparamos precios de la canasta básica en mercados, supermercados y tiendas de barrio de la Ciudad de México para recomendar dónde comprar con $1,500 a la semana, con el transporte incluido.

Proyecto del grupo 7AM1 para Modelos Econométricos, ESCOM-IPN. Entrega final: 5 de diciembre de 2026.

## Qué vamos a entregar

| Producto | Comité | Fecha |
|---|---|---|
| Dataset con al menos 3,000 precios válidos, cada uno con foto | Datos | 30 nov |
| Estudio econométrico: regresión múltiple, dicotómicas, panel y supuestos | Econometría | 2 dic |
| Comparación de algoritmos de pronóstico contra el último precio | Predicción | 2 dic |
| Aplicación web que recomienda dónde comprar | Aplicación | 3 dic |
| Artículo técnico | Artículo | 4 dic |

## Qué te toca

**Todos recolectan.** Tu código de recolector (por ejemplo E3-04) y tus establecimientos están en la matriz de responsabilidades de la planeación. Antes de salir lee el [manual de recolección](docs/manual_recoleccion.md). Para recolectar no necesitas Git.

**Todos están en un comité.** Cada comité trabaja en su rama y en su carpeta (ver la tabla de abajo).

| Equipo | Zona | Comité que coordina el líder |
|---|---|---|
| 1 | Norte y 3 establecimientos de Cuauhtémoc | Datos |
| 2 | Oriente y 2 de Cuauhtémoc | Econometría |
| 3 | Sur y 2 de Benito Juárez | Predicción |
| 4 | Poniente y 2 de Benito Juárez | Aplicación |

## Calendario

| Ronda | Fechas | Precios válidos acumulados |
|---|---|---|
| Piloto | 22 y 23 oct | No cuenta |
| 1 | 24 y 25 oct | 500 |
| 2 | 31 oct y 1 nov | 1,000 |
| 3 | 7 y 8 nov | 1,500 |
| 4 | 14 y 15 nov | 2,000 |
| 5 | 21 y 22 nov | 2,500 |
| 6 | 28 y 29 nov | 3,000 |

Visitas sábado o domingo de 9:00 a 13:00. Cada lunes hay revisión y el comité de datos publica el reporte de cobertura.

## Dónde va cada cosa

| Carpeta | Qué contiene | Quién la modifica |
|---|---|---|
| `datos/original/` | Un CSV por ronda y equipo, tal como sale del formulario. Nunca se edita | Comité de datos |
| `datos/catalogos/` | Productos, establecimientos, rutas y tarifas | Comités de datos y aplicación |
| `datos/trabajo/` | `precios.csv` con todo unido y normalizado | Solo los scripts |
| `datos/externos/` | Histórico de PROFECO y serie del INPC | Comité de predicción |
| `datos/diccionario.md` y `datos/bitacora.md` | Qué significa cada variable y cada corrección hecha | Comité de datos |
| `reportes/cobertura/` | Reporte semanal de precios válidos | Solo los scripts |
| `scripts/` y `tests/` | Validación, normalización, integración y cobertura | Comité de datos |
| `notebooks/` | Exploratorio, modelos, supuestos y pronósticos | Comités de econometría y predicción |
| `modelos/` | Pronósticos y métricas | Comité de predicción |
| `app/` | Aplicación | Comité de aplicación |
| `articulo/` | Artículo y figuras | Comité de artículo |
| `docs/` | Manual de recolección, planeación y minutas | Líderes |

## Cómo trabajamos

1. `main` solo recibe cambios por pull request y lo revisa alguien de otro equipo.
2. Cada comité trabaja en su rama: `datos`, `econometria`, `prediccion`, `app` y `articulo`.
3. Solo el comité de datos sube archivos a `datos/original/`.
4. Al cerrar cada ronda se marca una etiqueta, por ejemplo `ronda-02`.
5. Cada tarea es un issue asignado a una persona con fecha en la pestaña Projects.

Para trabajar en tu rama:

```bash
git clone https://github.com/Angel-Eduardo-Reyes-Leon/canasta-cdmx.git
cd canasta-cdmx
git checkout econometria          # la rama de tu comité
git pull                          # antes de empezar, trae lo último
git add notebooks/02_modelo1.ipynb
git commit -m "Agrega la especificación M1a"
git push
```

Cuando tu parte esté lista, en GitHub abre un pull request de tu rama hacia `main` y pide revisión a alguien de otro equipo. La validación y las pruebas corren solas y tienen que salir en verde.

## Instalar y correr

```bash
python -m venv .venv
source .venv/bin/activate         # en Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Cada ronda, el comité de datos corre:

```bash
python scripts/validar.py --ronda 2   # revisa los CSV de datos/original
python scripts/integrar.py            # genera datos/trabajo/precios.csv
python scripts/cobertura.py           # genera el reporte de la semana
pytest                                # pruebas
```

Un error en los datos se corrige con una fila en `datos/bitacora.md`, nunca editando `datos/original/`.

## Reglas

- Ningún precio se inventa ni se rellena. Lo que no se encontró queda sin precio.
- Los precios vistos en internet no cuentan.
- En el repositorio no van nombres ni fotos. Cada integrante aparece con su código y las fotos van a la carpeta de Drive del equipo.
