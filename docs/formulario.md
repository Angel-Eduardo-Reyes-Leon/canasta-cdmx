# Formulario de captura

Todos capturan en el mismo formulario de Google. Una respuesta es un producto en un establecimiento. Al exportar, la hoja tiene que salir con las columnas de `datos/plantilla_captura.csv`, en ese orden.

## Preguntas

El título de cada pregunta es el nombre de la variable, así la hoja de respuestas ya trae los encabezados correctos.

| Pregunta | Tipo | Opciones o regla |
|---|---|---|
| fecha | Fecha | |
| ronda | Lista | 1 a 6 |
| hora | Hora | |
| reprogramada | Lista | 0, 1 |
| equipo | Lista | 1 a 4 |
| id_recolector | Lista | E1-01 a E4-06 |
| id_establecimiento | Lista | Los 45 códigos del catálogo |
| id_puesto | Respuesta corta | Solo en mercados |
| id_producto | Lista | P01 a P16 con el nombre, por ejemplo P03 Arroz |
| estado | Lista | disponible, agotado, no_manejado, no_visitado |
| precio_etiqueta | Respuesta corta | Número mayor que cero |
| cantidad_presentacion | Respuesta corta | Número |
| unidad_presentacion | Lista | g, kg, ml, L, pieza |
| marca | Respuesta corta | |
| tipo_marca | Lista | lider, propia, generica, granel |
| promocion | Lista | 0, 1 |
| tipo_promocion | Lista | ninguna, directa, 2x1, 3x2, multiple, tarjeta |
| condicion_promocion | Respuesta corta | |
| precio_regular | Respuesta corta | Número |
| fuente | Lista | presencial, en_linea |
| foto | Respuesta corta | Nombre del archivo, por ejemplo S-SUP-01-P06-R2.jpg |
| observaciones | Párrafo | |

Las preguntas de precio, presentación, marca y promoción van en una sección aparte. Si el estado no es disponible, el formulario salta esa sección y la fila queda sin precio.

Con la opción de vínculo prellenado, cada recolector recibe un enlace por establecimiento con ronda, equipo, código y establecimiento ya puestos. Así en cada producto solo elige el producto y llena el precio.

## Exportación

Cada domingo en la noche el comité de datos:

1. Filtra la hoja por ronda y equipo.
2. Borra la columna Marca temporal, deja la fecha como AAAA-MM-DD y en id_producto deja solo el código, por ejemplo P03.
3. Descarga el CSV con el nombre `ronda_02_equipo3.csv` y lo sube a `datos/original/` en la rama `datos`.
4. Corre `python scripts/validar.py --ronda 2` y abre el pull request.

Las credenciales y el enlace de edición del formulario no se suben al repositorio.
