# Manual de recolección

## Antes de salir

- Tus establecimientos y tu código están en la matriz de la planeación. Cada establecimiento se visita siempre el mismo día, sábado o domingo, entre 9:00 y 13:00.
- Lleva el celular con batería y el formulario abierto.
- En el piloto (22 y 23 de octubre) se confirma que cada establecimiento exista y abra en ese horario, dos integrantes capturan el mismo lugar para comparar criterios y se pesan paquetes de huevo de 12, 18 y 30 piezas para sacar las piezas por kilo.

## En el establecimiento

- Registra la opción más barata por kilo o litro que cumpla la especificación, en una presentación de entre la mitad y el doble de la de referencia. En el arroz entran bolsas de 500 g a 2 kg.
- En mercados usa siempre el mismo puesto para cada producto y anota su número o nombre.
- Toma foto de la etiqueta o del letrero. El archivo se llama `S-SUP-01-P06-R2.jpg`: establecimiento, producto y ronda.
- Si no hay etiqueta, pregunta el precio sin negociar y anótalo en observaciones.
- Anota la cantidad y la unidad como vienen en el empaque: 900 ml, 140 g, 18 piezas. El precio por kilo lo calcula el script.
- La promoción vale 1 solo si el descuento está a la vista y lo puede usar cualquiera. Se registra el precio que paga cualquier cliente por una unidad.

| Estado | Cuándo | ¿Lleva precio? |
|---|---|---|
| disponible | se encontró | sí |
| agotado | lo venden, pero ese día no había | no |
| no_manejado | no lo venden | no |
| no_visitado | la visita no se hizo | no |

## Después de la visita

- Captura los 16 productos de cada establecimiento, aunque no estén disponibles. Si no había señal, captura ese mismo día con las fotos.
- Sube las fotos ese día a la carpeta de Drive de tu equipo.

## Si no puedes ir

1. Avisa a tu equipo para que otro integrante cubra la visita.
2. Si nadie puede, se hace el otro día del mismo fin de semana, por la mañana.
3. Supermercados y tiendas de barrio se pueden reponer el lunes por la tarde, con reprogramada = 1. Los mercados no.
4. Si no se hace, la fila queda como no_visitado.

Si un establecimiento cerró, avisa a tu líder. Se cambia por otro del mismo tipo y alcaldía y se anota en la bitácora.

## Nunca

- Inventar un precio o copiarlo de otra semana.
- Cambiar de marca o presentación sin registrarlo.
- Registrar como presencial un precio visto en internet.
