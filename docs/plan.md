# Plan del proyecto

## Problema

Una familia de cuatro personas con $1,500 semanales para alimentos no sabe cuánto le cuesta su lista completa en cada comercio cercano, si lo que ahorra en un mercado compensa el pasaje, ni cuánto margen le queda si los precios suben. Queremos encontrar dónde comprar cada producto para que la suma de alimentos y transporte sea la más baja y saber si esa suma cabe en el presupuesto.

Las conclusiones valen para los 45 establecimientos observados. No es una muestra aleatoria de la ciudad y así lo vamos a reportar.

## Preguntas

1. ¿Cuánto cuesta la canasta semanal en cada establecimiento y en cada zona? ¿En cuántos casos cabe en $1,500?
2. ¿Qué diferencia porcentual hay entre mercado, supermercado y tienda de barrio para un mismo producto?
3. ¿La ventaja de los mercados es mayor en frutas, verduras, pollo, huevo y tortilla que en abarrotes?
4. ¿Cuándo conviene visitar dos o tres comercios en lugar de uno, ya con el pasaje sumado?
5. ¿Qué establecimientos y productos tienen precios más estables de una semana a otra?
6. ¿Cuánto sube la canasta si los alimentos aumentan 5 %, 10 % o 20 % y a partir de qué aumento ya no alcanza?
7. ¿Las promociones bajan de verdad el precio por kilo o por litro?
8. ¿Una canasta idéntica cuesta distinto según la zona o la alcaldía?
9. ¿Qué modelo predice mejor el precio de la semana siguiente frente al último precio conocido?

## Datos

- 16 productos, con 4 de reserva. Lista en `datos/catalogos/productos.csv`.
- 45 establecimientos, 9 por zona: 3 mercados públicos, 3 supermercados y 3 tiendas de barrio. Con la misma cuota en cada zona, el tipo de comercio no se confunde con la zona.
- 6 rondas de fin de semana. Cada establecimiento se visita siempre el mismo día entre 9:00 y 13:00.
- 16 x 45 x 6 = 4,320 registros programados. Para llegar a 3,000 precios válidos basta 69.4 % de cobertura. Esperamos alrededor de 3,670.

Si después de la ronda 3 hay menos de 1,500 válidos, desde la ronda 4 entran un establecimiento de reserva por zona y los 4 productos de reserva.

## Modelos econométricos

La variable dependiente es el logaritmo del precio por kilo o litro, así cada coeficiente se lee como diferencia porcentual. Todas las pruebas usan errores agrupados por establecimiento y significancia de 0.05.

| Modelo | Qué es | Qué responde |
|---|---|---|
| 1. Regresión múltiple | Tipo de comercio, promoción, tipo de marca, tamaño del empaque, distancia al transporte, zona, producto y ronda. Tres especificaciones anidadas (M1a, M1b y M1c) comparadas con prueba F, AIC y BIC | Preguntas 2, 7 y 8 |
| 2. Variables dicotómicas | El modelo 1 más la interacción entre tipo de comercio y producto perecedero | Pregunta 3 |
| 3. Datos de panel | Efectos fijos de producto y establecimiento y de ronda, estimado como regresión con dummies. Prueba F contra el modelo 1 | Pregunta 5 y cambios entre semanas |
| Supuestos | Normalidad, heterocedasticidad, multicolinealidad (VIF), autocorrelación, atípicos y forma funcional, cada uno con su decisión fijada de antemano | Validez de los tres modelos |

Las categorías base son mercado público, marca genérica o granel, zona Centro, tortilla y ronda 1.

| Hipótesis | Prueba |
|---|---|
| H1. Los tipos de comercio cobran distinto por un mismo producto | F, modelo 1 |
| H2. La ventaja del mercado frente al supermercado es mayor en perecederos | t de una cola, modelo 2 |
| H3. La tienda de barrio cobra más que el supermercado | t de una cola, modelo 1 |
| H4. La promoción baja el precio | t de una cola, modelos 1 y 3 |
| H5. Un empaque mayor tiene menor precio por unidad | t de una cola, modelo 1 |
| H6. Una misma canasta cuesta distinto según la zona | F, modelo 1 |
| H7. Hay cambios comunes de precio entre semanas | F, modelo 3 |
| H8. Los perecederos cambian más de una semana a otra que los abarrotes | F de igualdad de varianzas |

## Pronóstico de la siguiente ronda

| Método | Para qué |
|---|---|
| Último precio conocido | Referencia. Es lo que haría una familia sin modelo |
| Ajuste parcial con rezagos, estimado con Ridge | El precio de la semana depende del anterior |
| Random forest | Capta interacciones entre producto, comercio y tendencia |
| Chronos-2 sin reentrenar | Prueba si un modelo preentrenado compensa series de seis puntos |

Ridge y random forest se entrenan con nuestras rondas y, en una segunda variante, con el histórico de PROFECO (Quién es Quién en los Precios). La validación respeta el tiempo: se entrena con R2 y R3 para predecir R4, con R2 a R4 para predecir R5 y la ronda 6 se usa una sola vez al final. Comparamos con MAE, RMSE y MAPE. Un modelo solo sirve si su MAE es menor que el del último precio. Si ninguno lo logra, la aplicación usa el último precio y lo reportamos así.

## Recomendación de compra

Para cada origen la aplicación prueba todas las combinaciones de uno, dos o tres comercios de la zona y elige la de menor costo de alimentos más transporte. Compra paquetes completos y marca los productos que falten. El transporte se cobra por tramo: menos de 1 km a pie, de 1 a 5 km un pasaje y más de 5 km dos pasajes. El resultado se verifica contra un modelo de programación entera resuelto con PuLP.

Para medir el ahorro comparamos el plan recomendado contra comprar todo en el supermercado más cercano al origen.

## Entregables

| Producto | Terminado cuando | Comité | Fecha |
|---|---|---|---|
| 1. Dataset documentado | Al menos 3,000 precios válidos de las 5 zonas y 10 alcaldías, cada uno con foto y recolector | Datos | 30 nov |
| 2. Estudio econométrico | Modelos 1 a 3 e hipótesis H1 a H8 con estadístico, p-value y decisión | Econometría | 2 dic |
| 3. Comparación de algoritmos | Tabla comparativa en la ronda 6 y modelo operativo justificado | Predicción | 2 dic |
| 4. Aplicación | Publicada, con pruebas de la optimización que coinciden con PuLP | Aplicación | 3 dic |
| 5. Artículo | Revisado por los cuatro líderes y coherente con los productos 1 a 4 | Artículo | 4 dic |

La entrega final es el 5 de diciembre.

## Organización

Cada integrante pertenece a un equipo, con el que recolecta los precios de sus establecimientos, y a un comité, con el que hace una parte del sistema para todo el grupo. Cada equipo pone un integrante en cada comité. La asignación por código está en [asignacion.md](asignacion.md).

| Comité | Entregas parciales |
|---|---|
| Datos | Formulario y manual (22 oct), scripts y revisión automática (30 oct), integración y cobertura (cada lunes), dataset cerrado (30 nov), diccionario y bitácora finales (4 dic) |
| Econometría | Exploratorio (12 nov), modelos 1 y 2 preliminares (20 nov), panel preliminar (24 nov), modelos finales (2 dic) |
| Predicción | PROFECO e INPC limpios (30 oct), variables y referencia (13 nov), pliegue R4 (17 nov), pliegue R5 y modelo operativo (24 nov), comparación final (2 dic) |
| Aplicación | Seis vistas y tarifas (6 nov), optimizador con pruebas (13 nov), versión integrada (27 nov), publicada (3 dic) |
| Artículo | Estructura (6 nov), antecedentes (13 nov), metodología (20 nov), borrador (27 nov), final (4 dic) |

Los modelos se escriben primero con las rondas que haya y la versión final solo vuelve a correr el mismo código con las seis.

## Revisiones semanales

Cada lunes cada comité muestra su avance y los líderes lo anotan en una minuta en `docs/minutas/`. Si el lunes es asueto, la revisión pasa al día siguiente.

| Fecha | Qué se revisa |
|---|---|
| 26 oct | Ronda 1 integrada |
| 3 nov | Ronda 2, catálogo con coordenadas, scripts y PROFECO limpio |
| 9 nov | Control 1: al menos 1,500 válidos |
| 17 nov | Optimizador y prototipo con datos reales |
| 23 nov | Control 2: al menos 2,500 válidos, resultados preliminares |
| 30 nov | Cierre: al menos 3,000 válidos. Cada integrante explica una parte que no hizo |
