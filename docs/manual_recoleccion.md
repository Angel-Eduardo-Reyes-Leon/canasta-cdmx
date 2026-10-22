# Manual de recolección

## Antes de la ronda 1

Cada equipo hace un piloto el 22 o el 23 de octubre. El piloto no cuenta como ronda.

1. **Confirmar los establecimientos.** Revisa que cada uno exista, que venda la mayoría de los productos y que abra el sábado o el domingo entre 9:00 y 13:00. Si no cumple, se toma el más cercano del mismo tipo que sí cumpla.
2. **Llenar el catálogo.** Por cada establecimiento se anota en `datos/catalogos/establecimientos.csv` el nombre, subtipo, cadena, colonia, domicilio, si acepta tarjeta y el día de visita (sábado o domingo). Las coordenadas y distancias se completan a más tardar el 30 de octubre.
3. **Doble captura.** Dos integrantes registran el mismo establecimiento por separado y comparan. Las diferencias de criterio se corrigen ahora, antes de que haya datos reales.
4. **Factor del huevo.** Pesa un paquete de 12, uno de 18 y uno de 30 piezas, resta el peso del empaque y divide las piezas entre los kilos. El promedio de los tres va en la columna `factor_piezas_kg` de `productos.csv`.

### Cómo se eligen

| Tipo | Criterio |
|---|---|
| Mercado público | Del sistema de mercados de la Ciudad de México, con puestos fijos de frutas, verduras, pollo y abarrotes |
| Supermercado | Tienda de cadena con precios a la vista. En cada zona al menos una cadena tradicional y una bodega de descuento, y ninguna cadena más de dos veces |
| Tienda de barrio | Abarrotes independiente con recaudería que en el piloto venda al menos 10 de los 16 productos |

Supermercados y tiendas de barrio son los más cercanos por calle al punto de referencia de su alcaldía, dentro de 3 km. Los mercados candidatos son:

| Alcaldía | Punto de referencia | Mercados candidatos |
|---|---|---|
| Gustavo A. Madero | Metro Deportivo 18 de Marzo | Lindavista, Martín Carrera |
| Azcapotzalco | Metro Azcapotzalco | Mercado de Azcapotzalco |
| Cuauhtémoc | Metro Centro Médico | Medellín (equipo 1), Abelardo L. Rodríguez (equipo 2) |
| Benito Juárez | Metro Etiopía | Portales |
| Iztapalapa | Metro Constitución de 1917 | Santa Cruz Meyehualco y el más cercano al Metro |
| Iztacalco | Metro Santa Anita | Santa Anita |
| Coyoacán | Metro Universidad | Coyoacán, Santo Domingo |
| Tlalpan | Metrobús Fuentes Brotantes | Mercado de la Paz |
| Álvaro Obregón | Metro Observatorio | Melchor Múzquiz y el más cercano al Metro |
| Miguel Hidalgo | Metro Tacuba | Tacuba |

## Antes de salir

- Tus establecimientos están en [asignacion.md](asignacion.md) y su día de visita en el catálogo. Cada uno se visita siempre el mismo día entre 9:00 y 13:00.
- Lleva el celular con batería y el enlace del formulario abierto.

## En el establecimiento

- Busca cada producto del catálogo. Registra la opción más barata por kilo o litro que cumpla la especificación y que venga en una presentación de entre la mitad y el doble de la de referencia. En el arroz, por ejemplo, entran bolsas de 500 g a 2 kg.
- En mercados usa siempre el mismo puesto para cada producto y anota su número o nombre.
- Toma foto de la etiqueta o del letrero del precio. El archivo se llama con el establecimiento, el producto y la ronda: `S-SUP-01-P06-R2.jpg`.
- Si el producto no tiene etiqueta, pregunta el precio sin negociar y escríbelo en observaciones.
- Anota la cantidad y la unidad tal como vienen en el empaque, por ejemplo 900 ml, 140 g o 18 piezas. El precio por kilo o litro lo calcula el script.

## Promociones

- La promoción vale 1 solo si el descuento está a la vista y lo puede usar cualquier comprador. Anota el tipo, el precio regular si aparece y las condiciones.
- Las ofertas con tarjeta o por compra de varias piezas se anotan, pero el precio que se registra es el que paga cualquier cliente por una unidad.

## Estado de cada producto

| Estado | Cuándo |
|---|---|
| disponible | se encontró y tiene precio |
| agotado | el establecimiento lo vende, pero ese día no había |
| no_manejado | el establecimiento no lo vende |
| no_visitado | la visita no se hizo |

Solo los disponibles llevan precio.

## Después de la visita

- Sube las fotos ese mismo día a la carpeta de Drive de tu equipo.
- Revisa que hayas capturado los 16 productos de cada establecimiento, aunque no estén disponibles.

## Si no puedes ir

1. Avisa a tu equipo para que otro integrante cubra la visita ese fin de semana.
2. Si nadie puede, se repone el otro día del mismo fin de semana, también por la mañana.
3. En supermercados y tiendas de barrio se puede reponer el lunes por la tarde, antes de que se integre la ronda, marcando reprogramada = 1.
4. En mercados no hay reposición entre semana. La fila queda como no_visitado.

## Si no hay señal

Toma todas las fotos y captura los precios ese mismo día a partir de ellas.

## Si un establecimiento cierra

Se sustituye por otro del mismo tipo y la misma alcaldía, con un código nuevo, y se anota en la bitácora con fecha y motivo. Si desaparece un puesto de mercado, se cambia a otro del mismo mercado y se registra el nuevo id_puesto.

## Nunca

- Inventar un precio o copiarlo de otra semana.
- Cambiar de marca o de presentación sin registrarlo.
- Registrar como presencial un precio visto en internet.
