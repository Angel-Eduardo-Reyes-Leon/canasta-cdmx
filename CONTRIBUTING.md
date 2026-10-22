# Cómo colaborar

Esto es para quien trabaja en un comité. Para recolectar precios no hace falta Git, basta el [manual](docs/manual_recoleccion.md).

## Antes de empezar

1. Crea una cuenta en GitHub y pásale tu usuario al líder de tu equipo para que te invite.
2. Acepta la invitación desde el correo o desde https://github.com/notifications.
3. Instala Git y configura tu nombre y tu correo una sola vez:

   ```bash
   git config --global user.name "Tu nombre"
   git config --global user.email "el correo de tu cuenta de GitHub"
   ```

4. Clona el repositorio e instala las librerías:

   ```bash
   git clone https://github.com/Angel-Eduardo-Reyes-Leon/canasta-cdmx.git
   cd canasta-cdmx
   python -m venv .venv
   source .venv/bin/activate        # en Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

La primera vez que subas algo se abre el navegador para iniciar sesión en GitHub.

## Ramas

`main` es la versión revisada y nadie sube directo a ella. Cada comité trabaja en su rama:

| Rama | Comité |
|---|---|
| `datos` | Datos: formulario, catálogos, scripts, rondas y bitácora |
| `econometria` | Econometría: exploratorio, modelos 1 a 3 y supuestos |
| `prediccion` | Predicción: PROFECO, INPC, pronósticos y métricas |
| `app` | Aplicación |
| `articulo` | Artículo |

## Trabajo de cada día

Cámbiate a la rama de tu comité y trae lo último:

```bash
git checkout econometria
git pull
git merge origin/main
```

Haz tus cambios y guárdalos:

```bash
git add notebooks/02_modelo1_regresion.ipynb
git commit -m "Agrega la especificación M1a del modelo 1"
git push
```

Agrega solo los archivos que cambiaste, no la carpeta entera. Un commit es un cambio con sentido propio. El mensaje dice qué cambia, en presente y en pocas palabras. Los datos de una ronda llevan ronda, equipo y número de registros: `Ronda 2, equipo 3, 176 registros`.

## Pull requests

Cuando una parte está lista para entrar a `main`:

1. En GitHub ve a **Pull requests** y luego **New pull request**.
2. Elige `base: main` y `compare:` la rama de tu comité.
3. Llena la plantilla. Si resuelve un issue, escribe `Cierra #12` para que se cierre solo.
4. Pide revisión a alguien de otro equipo en **Reviewers**.

GitHub corre la validación de datos y las pruebas. Si salen en rojo, abre el detalle en la pestaña **Checks**, corrige en tu rama y vuelve a subir. El pull request se actualiza solo.

## Revisar un pull request

Cada integrante revisa al menos un pull request de otro equipo por semana.

1. Abre la pestaña **Files changed** y lee los cambios.
2. Deja comentarios en la línea que corresponda si algo no está claro o está mal.
3. Al terminar elige **Approve** o **Request changes**.

Revisa que los datos coincidan con la evidencia, que el código corra y que no haya nombres, fotos ni credenciales.

## Issues y tablero

Cada tarea es un issue con una persona asignada y una fecha. El tablero del proyecto en la pestaña **Projects** muestra qué está pendiente, en curso y terminado. Si cambia una asignación, se anota en el issue.

## Lo que no se sube

- Fotos. Van a la carpeta de Drive del equipo.
- Nombres de integrantes. Se usa el código de recolector.
- Credenciales del formulario o de cualquier servicio.
- Archivos completos de PROFECO. Solo la parte filtrada a la Ciudad de México y a los 16 productos.

El `.gitignore` ya deja fuera fotos, credenciales y archivos temporales, pero revisa con `git status` antes de cada commit.
