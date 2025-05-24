from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from yt_dlp import YoutubeDL
import os
import random
import subprocess
from datetime import datetime

BOT_TOKEN = "7313122721:AAEwW42bwmfnQ_JuHgXlRpKkn6lUKf0shyY"

USUARIOS_AUTORIZADOS = [759118377, 6324370350]

# 🎬 Mensajes durante la descarga
MENSAJES_DESCARGANDO = [
    "🔧 Espera un momento, estoy bajando el video...",
    "Dame un segundo que esto está cocinándose 🎬",
    "Cargando la artillería... 💣",
    "Esto está que arde... 🔥",
    "Procesando con cariño cubano 🇨🇺",
    "Bajando como agua por el malecón 🌊",
    "Esto viene volando bajito ✈️",
    "Conectando el tubo del internet 🧪",
    "Estoy rompiendo la fibra óptica por ti 💥",
    "Aquí vamos, tirando bytes como loco 💾"
]

# 📦 Mensajes al enviar el video
MENSAJES_FINAL = [
    "📽️ Míralo aquí:",
    "🎉 Aquí lo tienes, papá:",
    "🧨 Toma fuego 🔥",
    "Te lo dejo servido 😎",
    "🎬 Disfrútalo que está calientico",
    "📦 Paquete entregado",
    "🚀 Directo desde los servidores"
]

# ⚠️ Cuando el usuario abusa
MENSAJES_EXCESO = [
    "😅 Pipo llevas una pila de videos, ¿qué tú te crees, que yo soy servidor premium?",
    "🐷 ¿Y tú vas a ver todo eso hoy?",
    "🧠 Bájale dos, que esto no es Netflix ilimitado.",
    "😤 Estás abusando ya chama.",
    "🤯 ¿Estás bajando para ti o pa toda la cuadra?"
]

# 📊 Conteo diario de enlaces
conteo_usuarios = {}

def actualizar_conteo(user_id):
    hoy = datetime.now().date()
    if user_id not in conteo_usuarios:
        conteo_usuarios[user_id] = {"fecha": hoy, "cantidad": 1}
    else:
        if conteo_usuarios[user_id]["fecha"] != hoy:
            conteo_usuarios[user_id] = {"fecha": hoy, "cantidad": 1}
        else:
            conteo_usuarios[user_id]["cantidad"] += 1
    return conteo_usuarios[user_id]["cantidad"]

def optimizar_video(input_file, output_file):
    subprocess.run([
        "ffmpeg",
        "-i", input_file,
        "-movflags", "+faststart",
        "-c", "copy",
        output_file
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# 🚀 /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in USUARIOS_AUTORIZADOS:
        await update.message.reply_text("⛔ No tienes permiso para usar este bot.")
        return
    await update.message.reply_text("👋 Envíame un link de Instagram, TikTok, Facebook o YouTube y te lo descargo.")

# 🎯 Mensajes con enlaces
async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in USUARIOS_AUTORIZADOS:
        await update.message.reply_text("⛔ No tienes permiso para usar este bot.")
        return

    cantidad_hoy = actualizar_conteo(user_id)

    await update.message.reply_text(random.choice(MENSAJES_DESCARGANDO))
    if cantidad_hoy > 5:
        await update.message.reply_text(random.choice(MENSAJES_EXCESO))

    url = update.message.text.strip()

    try:
        ydl_opts = {
            'outtmpl': '%(title).50s.%(ext)s',
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
            'merge_output_format': 'mp4',
            'quiet': True,
            'cookiefile': 'instagram_cookies.txt'  # opcional
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            if not filename.endswith(".mp4"):
                filename += ".mp4"

        # Optimizar video para móviles
        optimizar_video(filename, "final.mp4")

        await update.message.reply_text(random.choice(MENSAJES_FINAL))
        await update.message.reply_video(video=open("final.mp4", 'rb'))

        os.remove(filename)
        os.remove("final.mp4")
        print(f"✅ Video enviado a {user_id} y eliminado.")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")
        print("Error:", e)

# 🟢 Iniciar bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_link))

    print("🤖 Bot funcionando con compatibilidad para móviles y frases cubanas...")
    app.run_polling()
