#!/usr/bin/env bash

# Actualizar los paquetes
apt-get update

# Instalar ffmpeg (para que yt-dlp pueda fusionar video+audio)
apt-get install -y ffmpeg

# Instalar las dependencias de Python
pip install -r requirements.txt
