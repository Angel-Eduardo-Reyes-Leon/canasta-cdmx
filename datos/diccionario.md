# Diccionario de datos

## Archivos de datos/original

Un CSV por ronda y equipo, exportado del formulario. Una fila es un producto en un establecimiento en una ronda. Las columnas, en orden, están en `datos/plantilla_captura.csv`.

| Variable | Tipo | Valores o unidad | Descripción |
|---|---|---|---|
| fecha | fecha | AAAA-MM-DD | Día de la visita |
| ronda | entero | 1 a 6 | Fin de semana de recolección |
| hora | hora | HH:MM | Hora de la visita |
| reprogramada | 0 o 1 | | 1 si la visita se hizo fuera del día programado |
| equipo | entero | 1 a 4 | Equipo que captura |
| id_recolector | texto | E3-04 | Código del integrante |
| id_establecimiento | texto | S-SUP-01 | Código del catálogo de establecimientos |
| id_puesto | texto | | Puesto fijo, solo en mercados |
| id_producto | texto | P01 a P16 | Código del catálogo de productos |
| estado | texto | disponible, agotado, no_manejado, no_visitado | Disponibilidad del producto |
| precio_etiqueta | número | pesos | Precio de la presentación. Vacío si no está disponible |
| cantidad_presentacion | número | | Contenido del envase tal como viene |
| unidad_presentacion | texto | g, kg, ml, L, pieza | Unidad del envase |
| marca | texto | | Marca del empaque o no aplica |
| tipo_marca | texto | lider, propia, generica, granel | En los modelos generica y granel van juntas |
| promocion | 0 o 1 | | 1 si hay descuento directo para cualquier comprador |
| tipo_promocion | texto | ninguna, directa, 2x1, 3x2, multiple, tarjeta | |
| condicion_promocion | texto | | Requisito para la oferta, por ejemplo compra mínima |
| precio_regular | número | pesos | Precio sin descuento, si está a la vista |
| fuente | texto | presencial, en_linea | Los precios en línea no cuentan |
| foto | texto | S-SUP-01-P06-R2.jpg | Nombre del archivo de evidencia |
| observaciones | texto | | Aclaraciones |

## Columnas que agrega scripts/integrar.py

| Variable | Descripción |
|---|---|
| id_registro | Establecimiento, producto y ronda, por ejemplo S-SUP-01-P06-R2. No se puede repetir |
| unidad_base | kg, L o pieza, según el catálogo de productos |
| contenido_base | Contenido del envase en la unidad base |
| precio_normalizado | precio_etiqueta entre contenido_base |
| valido | 1 si el precio cuenta para el análisis |
| festiva | 1 en la ronda 2 (Día de Muertos) y en la ronda 4 (El Buen Fin) |

También se agregan producto, grupo, nombre del establecimiento, tipo de comercio, zona, alcaldía, coordenadas, distancia al transporte y equipo responsable.

## Precio válido

Cuenta para la meta de 3,000 si cumple todo esto:

- estado disponible y fuente presencial
- precio mayor que cero con presentación y unidad completas
- foto asociada
- identificador único
- sin errores en la validación

## Catálogo de productos (catalogos/productos.csv)

| Variable | Descripción |
|---|---|
| id_producto | P01 a P16. P17 a P20 son productos de reserva |
| producto, especificacion | Qué se registra |
| grupo | perecedero o abarrote |
| unidad_base | kg o L |
| presentacion_referencia | Presentación de referencia en la unidad base |
| cantidad_semanal | Cantidad de la canasta para cuatro personas |
| factor_piezas_kg | Piezas de huevo por kilo, medido en el piloto |
| activo | 1 si se recolecta |

## Catálogo de establecimientos (catalogos/establecimientos.csv)

| Variable | Descripción |
|---|---|
| id_establecimiento | Zona, tipo y número: N, C, O, S, P y MER, SUP, BAR |
| nombre, subtipo, cadena | Nombre comercial, subtipo (tradicional, bodega, descuento, abarrotes) y cadena |
| tipo_comercio | mercado, supermercado o barrio |
| zona, alcaldia, colonia, domicilio | Ubicación |
| latitud, longitud | Coordenadas para el mapa y el transporte |
| punto_referencia | Estación que sirve de origen en la alcaldía |
| dist_transporte_m | Metros por calle a la estación o parada más cercana |
| dist_referencia_km | Kilómetros por calle al punto de referencia |
| acepta_tarjeta | 0 o 1 |
| dia_visita | sábado o domingo |
| equipo_responsable | 1 a 4 |
| estado_catalogo | activo o sustituido |

Las distancias se miden por calle en un mapa en línea y se anota el método.
