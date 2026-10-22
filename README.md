# Canasta CDMX

Comparamos precios de la canasta básica en mercados, supermercados y tiendas de barrio de la Ciudad de México para recomendar dónde comprar con un presupuesto semanal de $1,500, con el costo del transporte incluido.

Proyecto del grupo 7AM1 para Modelos Econométricos, ESCOM-IPN.

Recolectamos precios de 16 productos en 45 establecimientos de las cinco zonas de la ciudad durante seis fines de semana, del 24 de octubre al 29 de noviembre de 2026. Con esos datos estimamos modelos de regresión con variables dicotómicas y datos de panel, comparamos algoritmos de pronóstico contra el último precio conocido y armamos una aplicación web. El plan completo, con preguntas, modelos, entregables y fechas, está en [docs/plan.md](docs/plan.md).

## Si vas a recolectar

No necesitas Git ni instalar nada.

1. Busca tu código de recolector y tus establecimientos en [docs/asignacion.md](docs/asignacion.md).
2. Lee el [manual de recolección](docs/manual_recoleccion.md) antes del piloto.
3. Captura en el formulario de Google del grupo y sube las fotos a la carpeta de Drive de tu equipo. Los enlaces los comparte el comité de datos en el grupo. No se publican aquí.

## Calendario de rondas

| Ronda | Fechas | Meta acumulada de precios válidos |
|---|---|---|
| Piloto | 22 y 23 de octubre | No cuenta |
| 1 | 24 y 25 de octubre | 500 |
| 2 | 31 de octubre y 1 de noviembre (Día de Muertos) | 1,000 |
| 3 | 7 y 8 de noviembre | 1,500 |
| 4 | 14 y 15 de noviembre (El Buen Fin) | 2,000 |
| 5 | 21 y 22 de noviembre | 2,500 |
| 6 | 28 y 29 de noviembre | 3,000 |

Las visitas son sábado o domingo entre 9:00 y 13:00. Cada lunes el comité de datos integra la ronda y publica el reporte de cobertura en `reportes/cobertura/`.

## Equipos y zonas

| Equipo | Zona completa | Establecimientos del Centro | Total | Comité que coordina |
|---|---|---|---|---|
| 1 | Norte (Gustavo A. Madero y Azcapotzalco) | 3 en Cuauhtémoc | 12 | Datos |
| 2 | Oriente (Iztapalapa e Iztacalco) | 2 en Cuauhtémoc | 11 | Econometría |
| 3 | Sur (Coyoacán y Tlalpan) | 2 en Benito Juárez | 11 | Predicción |
| 4 | Poniente (Álvaro Obregón y Miguel Hidalgo) | 2 en Benito Juárez | 11 | Aplicación |

El artículo lo coordinan los cuatro líderes.

## Si vas a trabajar en el repositorio

Cómo clonar, trabajar en la rama de tu comité y abrir un pull request está en [CONTRIBUTING.md](CONTRIBUTING.md). Para instalar:

```bash
git clone https://github.com/Angel-Eduardo-Reyes-Leon/canasta-cdmx.git
cd canasta-cdmx
python -m venv .venv
source .venv/bin/activate        # en Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Estructura

```
canasta-cdmx/
├── articulo/             borrador del artículo
├── datos/
│   ├── original/         un CSV por ronda y equipo, tal como sale del formulario
│   ├── catalogos/        productos, establecimientos, puntos de referencia, tarifas y rutas
│   ├── trabajo/          precios.csv, lo genera scripts/integrar.py
│   ├── externos/         histórico de PROFECO filtrado y serie del INPC de alimentos
│   ├── diccionario.md
│   ├── bitacora.md
│   └── plantilla_captura.csv
├── docs/                 plan, asignación, manual, formulario y minutas
├── reportes/cobertura/   reporte semanal de precios válidos
├── scripts/              validación, normalización, integración y cobertura
└── tests/
```

Cada comité agrega su parte en su rama conforme avanza el calendario:

| Carpeta | Comité | Desde |
|---|---|---|
| `notebooks/` con el análisis exploratorio y los modelos 1 a 3 | Econometría | 12 de noviembre |
| `notebooks/` con los pronósticos y `modelos/` | Predicción | 13 de noviembre |
| `app/` | Aplicación | 6 de noviembre |

Cada uno agrega sus librerías a `requirements.txt` en el mismo pull request.

## Flujo de cada ronda

1. Cada integrante visita sus establecimientos, captura los precios en el formulario y sube las fotos a la carpeta de su equipo.
2. El domingo en la noche el comité de datos exporta un CSV por equipo a `datos/original/` con el nombre `ronda_02_equipo3.csv`.
3. Se revisan los archivos:

   ```bash
   python scripts/validar.py --ronda 2
   ```

   Un error se corrige agregando una fila en `datos/bitacora.md`. El archivo de `datos/original/` no se edita.
4. El lunes se integran las rondas y se genera el reporte de cobertura:

   ```bash
   python scripts/integrar.py
   python scripts/cobertura.py
   ```

5. Se marca la ronda con una etiqueta, por ejemplo `git tag ronda-02`, para poder repetir cualquier resultado con los datos de esa fecha.

## Pruebas

```bash
pytest
```

Revisan la conversión de unidades y las reglas de validación. Corren solas en cada pull request junto con `scripts/validar.py`.

## Reglas de los datos

- Un registro es un producto en un establecimiento en una ronda.
- Agotados, no manejados y no visitados se registran sin precio. Ningún precio se inventa ni se rellena.
- Los precios vistos en línea se marcan con fuente `en_linea` y no cuentan para el análisis.
- Un precio es válido si el producto estaba disponible, se tomó en persona, tiene foto y su precio por kilo o litro es mayor que cero. La meta es de al menos 3,000 precios válidos.
- En el repositorio no van nombres. Cada integrante aparece con su código de recolector.

El detalle de cada variable está en [datos/diccionario.md](datos/diccionario.md).
