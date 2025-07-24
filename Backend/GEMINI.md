# Guía del Proyecto: MoneyPrinter Backend

## Descripción General

Este proyecto es un backend de Flask diseñado para automatizar la creación de videos cortos de estilo "social media". El proceso completo, desde la generación del guion hasta la producción del video final, es orquestado por una única llamada a la API. El sistema genera un guion, busca videos de stock relevantes, crea una voz en off, añade subtítulos y, opcionalmente, sube el video a YouTube.

## Flujo de Ejecución Principal

El núcleo de la aplicación reside en `main.py`. El proceso se inicia con una solicitud POST al endpoint `/api/generate`.

1.  **Recepción de la Solicitud**: `main.py` recibe los parámetros del video, como el tema, la voz deseada y otras configuraciones.
2.  **Generación de Guion**: Se llama a `gpt.py` para generar un guion de video basado en el tema proporcionado por el usuario, utilizando un modelo de IA (probablemente OpenAI).
3.  **Búsqueda de Videos**: `search.py` toma el guion, extrae términos de búsqueda y consulta a múltiples proveedores de video (Pexels, Pixabay) para encontrar clips de video de stock.
4.  **Descarga de Contenido**: Los URLs de los videos encontrados se utilizan para descargar los archivos de video, que se guardan en el directorio `temp/` en la raíz del proyecto.
5.  **Generación de Audio (TTS)**: `tiktokvoice.py` convierte cada oración del guion en audio (Text-to-Speech).
6.  **Generación de Subtítulos**: `video.py` utiliza los clips de audio y el guion para generar un archivo de subtítulos (`.srt`) a través de AssemblyAI o un método local.
7.  **Combinación de Video**: Los clips de video descargados se combinan en un único archivo de video sin audio.
8.  **Composición Final**: `video.py` ensambla el video final, combinando el clip de video, la pista de audio TTS y los subtítulos.
9.  **Subida a YouTube (Opcional)**: Si se solicita, `youtube.py` se encarga de subir el video final a YouTube, gestionando la autenticación a través de OAuth2.

## Estructura del Proyecto

```
MoneyPrinter/
├── Backend/
│   ├── main.py             # Servidor Flask principal y orquestador del flujo.
│   ├── search.py           # Lógica para buscar videos de stock en Pexels y Pixabay.
│   ├── video.py            # Funciones para descargar, combinar y generar el video final.
│   ├── gpt.py              # Generación de guion con IA.
│   ├── tiktokvoice.py      # Generación de audio Text-to-Speech.
│   ├── youtube.py          # Lógica para la subida de videos a YouTube.
│   ├── utils.py            # Funciones de utilidad (manejo de archivos, directorios, etc.).
│   ├── client_secret.json  # Credenciales de Google Cloud para la API de YouTube.
│   └── ...
├── temp/                   # Directorio para archivos de video y audio temporales.
├── subtitles/              # Directorio para los archivos de subtítulos generados.
├── Songs/                  # Directorio para la música de fondo.
└── .env                    # Archivo de configuración para todas las claves de API y rutas.
```

## Configuración Esencial

La configuración del proyecto se gestiona principalmente a través de un archivo `.env` y el archivo `client_secret.json`.

### 1. Archivo `.env`

Este archivo **debe estar ubicado en el directorio raíz del proyecto** (`D:\Projects\MoneyPrinter\.env`). Contiene todas las claves de API y configuraciones sensibles.

**Variables Requeridas:**
*   `PEXELS_API_KEY`: Tu clave de API de Pexels.
*   `PIXABAY_API_KEY`: Tu clave de API de Pixabay.
*   `TIKTOK_SESSION_ID`: El ID de sesión para el servicio de TTS de TikTok.
*   `IMAGEMAGICK_BINARY`: La ruta absoluta al ejecutable de ImageMagick (ej. `C:\Program Files\ImageMagick\magick.exe`).
*   `ASSEMBLY_AI_API_KEY`: (Opcional) Tu clave de API de AssemblyAI para la generación de subtítulos.
*   `OPENAI_API_KEY`: (Opcional) Tu clave de API de OpenAI para la generación de guiones.

### 2. Credenciales de YouTube

El archivo `client_secret.json` contiene las credenciales de OAuth 2.0 de Google Cloud. **Debe estar ubicado dentro del directorio `Backend`**. Se obtiene desde la consola de Google Cloud y es necesario para la subida automática de videos a YouTube.

## Cómo Ejecutar

1.  **Asegúrate de que todas las dependencias de Python estén instaladas.** (Ej. `pip install -r requirements.txt`).
2.  **Verifica que ImageMagick esté instalado** y que la ruta en el archivo `.env` sea correcta.
3.  **Asegúrate de que los archivos `.env` y `client_secret.json` estén en sus ubicaciones correctas** y contengan los valores adecuados.
4.  Navega al directorio `Backend` en tu terminal.
5.  Ejecuta el servidor Flask con el siguiente comando:
    ```bash
    python main.py
    ```
6.  El servidor se iniciará en `http://0.0.0.0:8080`. Puedes enviar una solicitud POST a `/api/generate` para comenzar el proceso de creación de video.
