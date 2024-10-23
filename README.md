# 📥 Python Video Downloader

Una aplicación de escritorio con interfaz gráfica para descargar videos y audio de YouTube y otros sitios web. Construida con Python, tkinter y yt-dlp.

![Python](https://img.shields.io/badge/Python-3.6+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![yt-dlp](https://img.shields.io/badge/yt--dlp-latest-red.svg)

## 🚀 Características

- ✨ Interfaz gráfica intuitiva y fácil de usar
- 📹 Descarga videos en múltiples calidades
- 🎵 Extracción de audio en formato MP3
- 📊 Barra de progreso en tiempo real
- 💨 Muestra velocidad de descarga
- 📂 Selección personalizada de directorio de descarga
- ℹ️ Información detallada del video
- 🔄 Soporte para múltiples formatos

## 📋 Requisitos Previos

- Python 3.6 o superior
- pip (gestor de paquetes de Python)

## 💻 Uso

1. Ejecuta la aplicación:
```bash
python video_downloader.py
```

2. Interfaz principal:
   - Ingresa la URL del video
   - Haz clic en "Obtener Info" para ver los detalles del video
   - Selecciona el formato de descarga deseado
   - Elige el directorio de descarga (opcional)
   - Haz clic en "Descargar Video" o "Descargar Audio"


## 📚 Dependencias

- yt-dlp: Para la descarga de videos
- tkinter: Para la interfaz gráfica
- threading: Para manejo de descargas asíncronas

## ⚙️ Configuración

El programa utiliza las siguientes configuraciones por defecto:

- Directorio de descarga: Carpeta "Downloads" del usuario
- Calidad de audio MP3: 192kbps
- Formato de video: Mejor calidad disponible según selección

## 🔧 Personalización

Puedes modificar las siguientes opciones en el código:

- Cambiar el tamaño de la ventana:
```python
self.root.geometry("700x500")
```

- Modificar la calidad del audio:
```python
'preferredquality': '192'  # Cambia a '320' para mejor calidad
```

## ⚠️ Notas importantes

- Asegúrate de tener una conexión estable a Internet
- Algunos videos pueden tener restricciones de descarga
- Respeta los derechos de autor y las políticas de uso
- Para videos de alta calidad, asegúrate de tener suficiente espacio en disco

## 🐛 Solución de problemas comunes

1. Error "HTTP Error 400: Bad Request"
   - Actualiza yt-dlp: `pip install --upgrade yt-dlp`

2. Error al descargar audio
   - Verifica que ffmpeg esté instalado en tu sistema

3. La interfaz no responde durante la descarga
   - Es normal, la descarga se ejecuta en segundo plano


## 🙏 Agradecimientos

- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [Python](https://www.python.org/)
- [tkinter](https://docs.python.org/3/library/tkinter.html)
