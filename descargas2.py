from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from yt_dlp import YoutubeDL
import os
import random
from datetime import datetime

BOT_TOKEN = "7313122721:AAEwW42bwmfnQ_JuHgXlRpKkn6lUKf0shyY"

USUARIOS_AUTORIZADOS = [759118377, 6324370350]

# Mensajes globales
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
    "Aquí vamos, tirando bytes como loco 💾",
    "Esto se está cociendo como congrí bien hecho 🍚",
    "Armando el video frame por frame 🧩",
    "Trayéndolo desde los servidores del cielo ☁️",
    "Dame 2 segundos que esto pesa como 3 arroz 🍱",
    "Lo tengo en la olla, casi está listo 👨‍🍳",
    "Esto va más rápido que un paquete en Revolico 📦",
    "Sacándole el jugo al link 🧃",
    "Desempolvando el HD con cariño 😌",
    "Esto baja más lento que cola de pollo... pero baja 🐔",
    "Montando el paquete como el sábado en la SNET 📡",
    "Estirando el cable hasta Silicon Valley 🌎",
    "Manejando el tráfico de datos como un yutong 🚍",
    "Ya viene bajando... como salario de cubano 💸",
    "Conectado al satélite ruso 🛰️",
    "Empacando bits en un cartucho 🎮",
    "Esto baja con estilo y sabrosura 💃",
    "Raspando la red como buen cubano 🧠",
    "Recibiendo el archivo con tremendo swing 🎷",
    "Lo estoy trayendo a puro pulmón 😮‍💨",
    "Ya está bajando, pero con visa americana 🛂"
]


MENSAJES_FINAL = [
    "📽️ Míralo aquí:",
    "🎉 Aquí lo tienes, papá:",
    "🧨 Toma fuego 🔥",
    "Listo, disfrútalo como el café de la abuela ☕",
    "Te lo dejo servido 😎",
    "💿 Ahí tienes tu joyita",
    "🎥 Esto es oro digital",
    "🎯 Misión cumplida, agente secreto",
    "🎬 Disfrútalo que está calientico",
    "😏 Te tengo malcriado, ahí va",
    "🤲 Toma, no digas que no te atiendo",
    "🎁 Entrega exprés a tu Telegram",
    "🔥 Caliente como pan recién salido del horno",
    "🚀 Directo desde los servidores",
    "🔓 Acceso desbloqueado a tu contenido",
    "💣 Este sí explota",
    "📦 Paquete entregado",
    "🍿 Siéntate y disfrútalo",
    "🧃 Tómalo con calma, sin atragantarte",
    "💌 Repartido con amor y WiFi robado",
    "🕹️ Tu contenido ha llegado, gamer",
    "🌴 Disfrútalo con brisa de Varadero",
    "🥳 Regalito descargado con estilo",
    "💼 Entregado como buen trabajador del mes",
    "📸 A tu medida, como selfie en filtro",
    "🧊 Está frío pero bueno",
    "📱 Descarga completada con flow",
    "🫡 A la orden, capitán de la red",
    "🚿 Limpiecito y listo para ver",
    "🔊 Sube el volumen y dale play"
]


MENSAJES_EXCESO = [
    "😅 Pipo llevas una pila de videos, ¿qué tú te crees, que yo soy servidor premium?",
    "🐷 ¿Y tú vas a ver todo eso hoy?",
    "🧠 Bájale dos, que esto no es Netflix ilimitado.",
    "😤 Estás abusando ya chama.",
    "😂 Oye pipo, dale un chance al servidor, que no soy robot de carga.",
    "📉 Ya tú bajaste más videos que el paquete entero",
    "👀 Oye, tú no trabajas ni nada no?",
    "😆 El bot ya se cansó, dale suave",
    "🛑 Esto no es para que abuses",
    "🍽️ Deja algo para mañana, que te vas a empachar",
    "📡 Estás gastando más ancho de banda que ETECSA en apagón",
    "📺 Pipo tú crees que esto es una antena satelital",
    "🤖 Ni un bot ruso descarga tanto",
    "📲 Te voy a poner cuota como Cubacel",
    "💣 Le estás metiendo más presión que al panadero del barrio",
    "🐌 Esto no es carrera de enlaces",
    "⚙️ Me vas a fundir el disco duro, chamaco",
    "💀 Esto no es zona WiFi gratis",
    "📶 ¿Tú sabes cuánto cuesta el mega fuera de Cuba?",
    "🥵 Me tienes sudando bits",
    "🤯 ¿Estás bajando para ti o pa toda la cuadra?",
    "📉 Tu plan de datos imaginario ya colapsó",
    "🧱 Me voy a desconectar si sigues así",
    "🎭 No seas descarado, deja algo pa mañana",
    "📊 Este ritmo no lo aguanta ni Google",
    "💬 Necesito vacaciones digitales contigo",
    "🚫 Tu cuota diaria se fue al piso",
    "🔋 Se me está acabando la batería de tanto trabajar",
    "🤐 Mejor no digo ná, solo bajo",
    "💀 Me dejaste sin RAM bro"
]


# Conteo diario
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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in USUARIOS_AUTORIZADOS:
        await update.message.reply_text("⛔ No tienes permiso para usar este bot.")
        return
    await update.message.reply_text("👋 Envíame un link de Instagram, TikTok o Facebook y te lo descargo.")

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in USUARIOS_AUTORIZADOS:
        await update.message.reply_text("⛔ No tienes permiso para usar este bot.")
        return

    # Contar enlaces
    cantidad_hoy = actualizar_conteo(user_id)

    await update.message.reply_text(random.choice(MENSAJES_DESCARGANDO))
    if cantidad_hoy > 5:
        await update.message.reply_text(random.choice(MENSAJES_EXCESO))

    url = update.message.text.strip()

    try:
        ydl_opts = {
            'outtmpl': '%(title).50s.%(ext)s',
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'quiet': True,
            'cookiefile': 'instagram_cookies.txt'
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            if not filename.endswith(".mp4"):
                filename += ".mp4"

        await update.message.reply_text(random.choice(MENSAJES_FINAL))
        await update.message.reply_video(video=open(filename, 'rb'))
        os.remove(filename)
        print(f"✅ Video enviado a {user_id} y eliminado.")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")
        print("Error:", e)

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_link))

    print("🤖 Bot funcionando con frases aleatorias...")
    app.run_polling()
