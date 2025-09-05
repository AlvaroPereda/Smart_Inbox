# Smart Inbox

Smart Inbox es una aplicación web que resume automáticamente los correos electrónicos recibidos en tu cuenta Gmail, mostrando los puntos principales de cada correo de forma clara y visual.

La aplicación utiliza el model-runner de Docker para procesar los correos con el modelo Llama 3.2, que cuenta con 3.21 billones de parámetros. Al ejecutar el proyecto por primera vez, el modelo se descargará automáticamente; este proceso puede tardar varios minutos según la velocidad de tu conexión a internet. Una vez descargado, todas las peticiones se procesan de forma local, sin enviar datos al exterior, garantizando privacidad.

## Requisitos
- Docker instalado en tu sistema.
- Acceso a una cuenta Gmail (debes configurar las variables en el archivo `.env`).
- Debes cumplir con los requisitos que pide model-runner de docker ([requisitos](https://docs.docker.com/ai/model-runner/#requirements))
- Git Bash (en Windows) para ejecutar el script `run.sh`.

## Instalación y ejecución
1. Configura el archivo `.env` con tus credenciales y parámetros:
   ```env
   EMAIL=tu_email@gmail.com
   PASSWORD=tu_contraseña()
   ```
   > **Importante:** Para la contraseña, debes crear una **Contraseña de aplicación de Google**. Esto es necesario porque Google no permite el acceso directo con la contraseña habitual en aplicaciones externas.
   >
   > Puedes crear tu contraseña de aplicación siguiendo estos pasos:
   > 1. Accede a la página de [Contraseñas de aplicación de Google](https://myaccount.google.com/apppasswords).
   > 2. Sigue las instrucciones para generar una contraseña específica para aplicaciones.
   > 3. Usa esa contraseña en el campo `PASSWORD` de tu archivo `.env`.
   >
   > Para más información sobre contraseñas de aplicación y cómo funcionan, consulta la [documentación oficial de Google](https://support.google.com/accounts/answer/185833?hl=es).
3. Ejecuta el script para construir y lanzar el contenedor:
   ```bash
   sh run.sh
   ```
   > **Nota:** En Windows, debes ejecutar este comando desde **Git Bash**. No funcionará correctamente en el CMD o PowerShell.

4. Accede a la aplicación en tu navegador en [http://localhost:8000](http://localhost:8000)

## Personalización
- Puedes modificar el archivo `system_prompt.txt` para ajustar el comportamiento y formato de los resúmenes generados por la IA.
- Los estilos y la lógica de la web pueden personalizarse en `static/style.css` y `static/app.js`.
