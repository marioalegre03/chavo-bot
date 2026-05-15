#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎪 CHAVO BOT - Bot de Trivia de El Chavo del Ocho para Telegram
producción - lee el token desde variable de entorno BOT_TOKEN
"""

import logging
import os
import random
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
)

# ─────────────────────────────────────────────
#  CONFIGURACIÓN
# ─────────────────────────────────────────────
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
if not BOT_TOKEN:
    raise RuntimeError("❌ Falta la variable de entorno BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────
#  ESTADOS DE CONVERSACIÓN
# ─────────────────────────────────────────────
ELEGIR_VERSION, EN_TRIVIA = range(2)

# ─────────────────────────────────────────────
#  IMÁGENES (URLs públicas)
# ─────────────────────────────────────────────
IMAGENES = {
    "bienvenida": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/El_chavo_del_ocho_title_card.jpg/640px-El_chavo_del_ocho_title_card.jpg",
    "original":   "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/El_chavo_del_ocho_title_card.jpg/640px-El_chavo_del_ocho_title_card.jpg",
    "animado":    "https://upload.wikimedia.org/wikipedia/en/thumb/7/71/ElChavoAnimado.jpg/220px-ElChavoAnimado.jpg",
    "fin":        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/El_chavo_del_ocho_title_card.jpg/640px-El_chavo_del_ocho_title_card.jpg",
}

# ─────────────────────────────────────────────
#  BANCO DE PREGUNTAS
# ─────────────────────────────────────────────
PREGUNTAS_ORIGINAL = [
    {
        "pregunta": "🛢️ ¿En qué objeto vive El Chavo?",
        "opciones": ["En una caja de cartón", "En un barril", "En una casita", "En un sótano"],
        "correcta": 1,
        "dato": "El Chavo vivía en el barril del número 8 de la vecindad 😄",
    },
    {
        "pregunta": "👨‍🏫 ¿Cómo se llama el maestro de la vecindad?",
        "opciones": ["Profesor Jirafales", "Maestro Cosme", "Don Ramón", "Señor Barriga"],
        "correcta": 0,
        "dato": "El Profesor Jirafales era el maestro y pretendiente de Doña Florinda 📚",
    },
    {
        "pregunta": "🤣 ¿Cuál es la frase más famosa del Chavo?",
        "opciones": ['"¡Esto, esto, esto!"', '"¡Fue sin querer queriendo!"', '"¡No me simpatizan!"', '"¡Cállate, cállate!"'],
        "correcta": 1,
        "dato": '"Fue sin querer queriendo" es la frase más icónica del Chavo 🎪',
    },
    {
        "pregunta": "🧒 ¿Cómo se llama el hijo de Doña Florinda?",
        "opciones": ["Ñoño", "Quico", "Godínez", "Jaimito"],
        "correcta": 1,
        "dato": "Quico, con su inseparable carrito y su característica risita 😂",
    },
    {
        "pregunta": "🏠 ¿Cómo se llama el dueño de la vecindad?",
        "opciones": ["Señor Barriga", "Don Ramón", "El Señor González", "Profesor Jirafales"],
        "correcta": 0,
        "dato": "El Señor Barriga siempre llegaba a cobrar la renta 💰",
    },
    {
        "pregunta": "💔 ¿Quién es la bruja del 71?",
        "opciones": ["Doña Florinda", "La Chilindrina", "Doña Clotilde", "Doña Nieves"],
        "correcta": 2,
        "dato": "Doña Clotilde, la vecina enamorada de Don Ramón 🧙‍♀️",
    },
    {
        "pregunta": "🍎 ¿Cuál es el apellido de Don Ramón?",
        "opciones": ["González", "García", "Vásquez", "Ortega"],
        "correcta": 0,
        "dato": "Don Ramón González Garza, padre de La Chilindrina 👴",
    },
    {
        "pregunta": "😜 ¿Cuál es el sobrenombre de la hija de Don Ramón?",
        "opciones": ["La Pesadilla", "La Traviesita", "La Chilindrina", "La Monita"],
        "correcta": 2,
        "dato": "La Chilindrina, con sus pecas y trenzas inconfundibles 🎀",
    },
    {
        "pregunta": "🎂 ¿Cuántos departamentos tiene la vecindad del Chavo?",
        "opciones": ["4", "6", "8", "10"],
        "correcta": 2,
        "dato": "La vecindad tenía 8 departamentos, de ahí el nombre 'del Ocho' 🏘️",
    },
    {
        "pregunta": "📺 ¿En qué año comenzó a transmitirse El Chavo del Ocho?",
        "opciones": ["1965", "1971", "1975", "1980"],
        "correcta": 1,
        "dato": "El Chavo del Ocho inició en 1971 en el canal 8 de Televisa 📡",
    },
    {
        "pregunta": "🎭 ¿Quién creó y dio vida a El Chavo del Ocho?",
        "opciones": ["Carlos Villagrán", "Rubén Aguirre", "Chespirito (Roberto Gómez Bolaños)", "Edgar Vivar"],
        "correcta": 2,
        "dato": "Roberto Gómez Bolaños, 'Chespirito', creó y actuó como El Chavo 🎬",
    },
    {
        "pregunta": "🧠 ¿Cómo se llama el niño gordito, hijo del Señor Barriga?",
        "opciones": ["Quico", "Ñoño", "Godínez", "El Chompiras"],
        "correcta": 1,
        "dato": "Ñoño era el hijo del Señor Barriga y el mejor amigo de Quico 🍕",
    },
    {
        "pregunta": "🌮 ¿Qué comida le encantaba al Chavo?",
        "opciones": ["Tortas de jamón", "Tacos de frijoles", "Enchiladas", "Tamales"],
        "correcta": 0,
        "dato": "¡Las tortas de jamón eran la debilidad del Chavo! 🥪",
    },
    {
        "pregunta": "🏫 ¿Cómo se llama el compañero de clase más flojo?",
        "opciones": ["El Chavo", "Quico", "Godínez", "Ñoño"],
        "correcta": 2,
        "dato": "Godínez era el clásico alumno que nunca traía la tarea 📝",
    },
    {
        "pregunta": "🎩 ¿Qué objeto siempre usaba El Chavo en la cabeza?",
        "opciones": ["Una boina", "Un sombrero de paja", "Un gorro de punto", "Una gorra de béisbol"],
        "correcta": 2,
        "dato": "El Chavo siempre usaba su inconfundible gorro de punto 🧢",
    },
]

PREGUNTAS_ANIMADO = [
    {
        "pregunta": "📺 ¿En qué año se estrenó El Chavo Animado?",
        "opciones": ["2000", "2004", "2006", "2010"],
        "correcta": 2,
        "dato": "El Chavo Animado se estrenó en 2006 como continuación de la serie original 🎬",
    },
    {
        "pregunta": "🎨 ¿Qué estudio de animación produjo El Chavo Animado?",
        "opciones": ["Disney", "Televisa / Lemon Studios", "Cartoon Network", "Nickelodeon"],
        "correcta": 1,
        "dato": "Televisa junto con Lemon Studios produjeron la serie animada 🏭",
    },
    {
        "pregunta": "🌍 ¿En cuántos países se transmitió El Chavo Animado?",
        "opciones": ["10 países", "20 países", "Más de 50 países", "Solo en México"],
        "correcta": 2,
        "dato": "El Chavo Animado se transmitió en más de 50 países del mundo 🌎",
    },
    {
        "pregunta": "🎤 ¿Quién dobló la voz de El Chavo en la serie animada?",
        "opciones": ["Chespirito", "Rubén Aguirre", "María Antonieta de las Nieves", "Florinda Meza"],
        "correcta": 2,
        "dato": "María Antonieta de las Nieves (La Chilindrina) dobló a El Chavo en la animada 🎙️",
    },
    {
        "pregunta": "🎭 ¿Cuántas temporadas tuvo El Chavo Animado?",
        "opciones": ["3", "5", "8", "10"],
        "correcta": 2,
        "dato": "El Chavo Animado tuvo 8 temporadas hasta el año 2014 📺",
    },
    {
        "pregunta": "🎡 ¿Cuál era el canal principal que transmitía El Chavo Animado en México?",
        "opciones": ["Canal 5", "Canal 2", "Canal 9", "Cartoon Network México"],
        "correcta": 0,
        "dato": "Canal 5 de Televisa fue el hogar de El Chavo Animado en México 📡",
    },
    {
        "pregunta": "🧒 En la versión animada, ¿qué nueva habilidad especial tenía El Chavo?",
        "opciones": ["Podía volar", "Tenía supervelocidad", "Sus travesuras siempre funcionaban sin querer", "Podía hablar con los animales"],
        "correcta": 2,
        "dato": "El espíritu del 'fue sin querer queriendo' se mantuvo en la animada 😄",
    },
    {
        "pregunta": "🎠 ¿Cuál fue el principal cambio visual entre la serie original y la animada?",
        "opciones": ["Los personajes eran adultos", "La vecindad estaba en una ciudad futurista", "Los personajes tenían diseño más caricaturesco y colorido", "El barril desaparecía"],
        "correcta": 2,
        "dato": "La animación permitió un estilo más caricaturesco preservando la esencia ✏️",
    },
    {
        "pregunta": "📅 ¿En qué año terminó la producción de El Chavo Animado?",
        "opciones": ["2010", "2012", "2014", "2016"],
        "correcta": 2,
        "dato": "La última temporada de El Chavo Animado fue en 2014 🎬",
    },
    {
        "pregunta": "🌟 ¿El Chavo Animado mantuvo los sketches de la vecindad?",
        "opciones": ["No, cambiaron todo el escenario", "Sí, la vecindad del Chavo siempre estuvo presente", "Solo aparecía en algunos episodios", "La reemplazaron por un parque"],
        "correcta": 1,
        "dato": "La icónica vecindad del Chavo fue el escenario principal de la animada 🏘️",
    },
    {
        "pregunta": "🎭 ¿Quién fue el creador de la historia de El Chavo Animado?",
        "opciones": ["Florinda Meza", "Carlos Villagrán", "Chespirito y su legado", "Un nuevo equipo de guionistas"],
        "correcta": 2,
        "dato": "La serie animada se basó completamente en el legado de Chespirito 🎪",
    },
    {
        "pregunta": "🏆 ¿Ganó El Chavo Animado algún premio importante?",
        "opciones": ["No ganó ninguno", "Ganó el Emmy Internacional", "Fue nominada al Annie Award", "Ganó el Ariel mexicano"],
        "correcta": 1,
        "dato": "El Chavo Animado ganó el Emmy Internacional como mejor animación 🏆",
    },
    {
        "pregunta": "🌎 ¿En qué idiomas fue doblada la serie animada?",
        "opciones": ["Solo español", "Español e inglés", "Español, inglés, portugués y más", "Solo se emitió en español"],
        "correcta": 2,
        "dato": "La serie fue doblada a múltiples idiomas para su emisión mundial 🌍",
    },
    {
        "pregunta": "📺 ¿Dónde se puede ver El Chavo Animado actualmente en streaming?",
        "opciones": ["Netflix", "Disney+", "VIX / ViX+", "Amazon Prime"],
        "correcta": 2,
        "dato": "VIX (antes Blim) tiene disponible El Chavo Animado en su catálogo 📱",
    },
    {
        "pregunta": "🎨 ¿Cuántos personajes nuevos se agregaron en la versión animada?",
        "opciones": ["Ninguno, solo los originales", "1 o 2 personajes secundarios", "Varios personajes nuevos en distintas temporadas", "Más de 20 personajes totalmente nuevos"],
        "correcta": 2,
        "dato": "Se introdujeron varios personajes nuevos a lo largo de las temporadas 🆕",
    },
]

# ─────────────────────────────────────────────
#  CONSTANTES DE SESIÓN
# ─────────────────────────────────────────────
KEY_VERSION   = "version"
KEY_PREGUNTAS = "preguntas"
KEY_INDICE    = "indice"
KEY_PUNTAJE   = "puntaje"
KEY_TOTAL     = "total"
NUM_PREGUNTAS = 10

# ─────────────────────────────────────────────
#  HANDLERS
# ─────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [
        [
            InlineKeyboardButton("📺 Original (1971)", callback_data="original"),
            InlineKeyboardButton("🎨 Animado (2006)",  callback_data="animado"),
        ],
        [InlineKeyboardButton("📊 Mi historial", callback_data="puntaje_historico")],
    ]
    await update.message.reply_photo(
        photo=IMAGENES["bienvenida"],
        caption=(
            "🎪 *¡Bienvenido al CHAVO BOT!* 🛢️\n\n"
            "🧡 El bot de trivia oficial de *El Chavo del Ocho*\n\n"
            "¿De qué versión quieres jugar? 👇"
        ),
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return ELEGIR_VERSION


async def elegir_version(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    if query.data == "puntaje_historico":
        historico = context.user_data.get("historico", [])
        if not historico:
            texto = "📊 Aún no tienes partidas guardadas. ¡Juega una primera! 🎮"
        else:
            lineas  = [f"• {v['version']}: {v['puntaje']}/{v['total']}" for v in historico[-5:]]
            promedio = sum(v["puntaje"]/v["total"]*100 for v in historico) / len(historico)
            texto   = f"📊 *Últimas partidas:*\n\n" + "\n".join(lineas) + f"\n\n📈 Promedio: {promedio:.0f}%"
        await query.edit_message_caption(caption=texto, parse_mode="Markdown")
        return ELEGIR_VERSION

    version = query.data
    context.user_data[KEY_VERSION] = version

    if version == "original":
        pool  = PREGUNTAS_ORIGINAL.copy()
        titulo = "📺 *Versión Original (1971-1992)*"
        foto   = IMAGENES["original"]
        desc   = "Preguntas sobre la serie clásica con Chespirito y el elenco original."
    else:
        pool  = PREGUNTAS_ANIMADO.copy()
        titulo = "🎨 *Versión Animada (2006-2014)*"
        foto   = IMAGENES["animado"]
        desc   = "Preguntas sobre la querida serie animada."

    random.shuffle(pool)
    context.user_data[KEY_PREGUNTAS] = pool[:NUM_PREGUNTAS]
    context.user_data[KEY_INDICE]    = 0
    context.user_data[KEY_PUNTAJE]   = 0
    context.user_data[KEY_TOTAL]     = NUM_PREGUNTAS

    await query.edit_message_media(
        media=InputMediaPhoto(
            media=foto,
            caption=(
                f"{titulo}\n\n_{desc}_\n\n"
                f"📋 *{NUM_PREGUNTAS} preguntas* aleatorias. ¡Suerte! 🧠"
            ),
            parse_mode="Markdown",
        )
    )
    await enviar_pregunta(update, context)
    return EN_TRIVIA


async def enviar_pregunta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    indice    = context.user_data[KEY_INDICE]
    preguntas = context.user_data[KEY_PREGUNTAS]
    total     = context.user_data[KEY_TOTAL]
    puntaje   = context.user_data[KEY_PUNTAJE]

    if indice >= total:
        await mostrar_resultado_final(update, context)
        return

    pregunta = preguntas[indice]
    letras   = ["🅰️", "🅱️", "🇨", "🇩"]
    teclado  = [
        [InlineKeyboardButton(f"{letras[i]} {op}", callback_data=str(i))]
        for i, op in enumerate(pregunta["opciones"])
    ]
    teclado.append([InlineKeyboardButton("🚪 Salir", callback_data="salir")])

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            f"🎪 *Pregunta {indice+1}/{total}  |  ⭐ {puntaje} pts*\n\n"
            f"❓ {pregunta['pregunta']}"
        ),
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(teclado),
    )


async def responder_pregunta(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    if query.data == "salir":
        await query.edit_message_text(
            text="👋 *¡Hasta la próxima!* Fue sin querer queriendo... 😄\n\nUsa /start para volver.",
            parse_mode="Markdown",
        )
        return ConversationHandler.END

    indice   = context.user_data[KEY_INDICE]
    pregunta = context.user_data[KEY_PREGUNTAS][indice]
    puntaje  = context.user_data[KEY_PUNTAJE]
    resp     = int(query.data)

    if resp == pregunta["correcta"]:
        context.user_data[KEY_PUNTAJE] = puntaje + 1
        texto = f"✅ *¡Correcto!* 🎉\n\n💡 _{pregunta['dato']}_"
    else:
        correcta_texto = pregunta["opciones"][pregunta["correcta"]]
        texto = f"❌ *¡Incorrecto!*\nEra: *{correcta_texto}*\n\n💡 _{pregunta['dato']}_"

    await query.edit_message_text(text=texto, parse_mode="Markdown")
    context.user_data[KEY_INDICE] = indice + 1

    prox = "🏆 Ver resultado" if context.user_data[KEY_INDICE] >= context.user_data[KEY_TOTAL] else "➡️ Siguiente"
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="👆 ¿Listo?",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(prox, callback_data="siguiente")]]),
    )
    return EN_TRIVIA


async def siguiente_pregunta(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.delete_message()
    await enviar_pregunta(update, context)
    return EN_TRIVIA


async def mostrar_resultado_final(update: Update, context: ContextTypes.DEFAULT_TYPE):
    puntaje = context.user_data[KEY_PUNTAJE]
    total   = context.user_data[KEY_TOTAL]
    version = context.user_data.get(KEY_VERSION, "original")
    pct     = (puntaje / total) * 100

    historico = context.user_data.get("historico", [])
    historico.append({"version": version.capitalize(), "puntaje": puntaje, "total": total})
    context.user_data["historico"] = historico

    if pct == 100:   calificacion = "🥇 ¡Perfecto! Eres un verdadero fan del Chavo!"
    elif pct >= 80:  calificacion = "🥈 ¡Excelente! Conoces muy bien la vecindad."
    elif pct >= 60:  calificacion = "🥉 ¡Bien! Pero puedes mejorar, ¿eh?"
    elif pct >= 40:  calificacion = "😅 ¿Seguro que ves El Chavo?"
    else:            calificacion = "😢 ¡Fue sin querer queriendo! Repasa más."

    keyboard = [
        [InlineKeyboardButton("🔄 Jugar de nuevo", callback_data="jugar_nuevo")],
        [InlineKeyboardButton("📊 Ver historial",  callback_data="ver_historial")],
    ]
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=IMAGENES["fin"],
        caption=(
            f"🎊 *¡Juego terminado!* 🎊\n\n"
            f"📊 *Resultado:* {puntaje}/{total} correctas\n"
            f"📈 *Porcentaje:* {pct:.0f}%\n\n"
            f"{calificacion}\n\n¿Qué quieres hacer? 👇"
        ),
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def jugar_nuevo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("📺 Original (1971)", callback_data="original"),
            InlineKeyboardButton("🎨 Animado (2006)",  callback_data="animado"),
        ],
    ]
    await query.edit_message_caption(
        caption="🎪 *¡Otra partida!*\n\n¿Qué versión eliges esta vez? 👇",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return ELEGIR_VERSION


async def ver_historial(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    historico = context.user_data.get("historico", [])
    if not historico:
        texto = "📊 No tienes partidas guardadas aún."
    else:
        lineas   = [f"• {v['version']}: {v['puntaje']}/{v['total']}" for v in historico[-5:]]
        promedio = sum(v["puntaje"]/v["total"]*100 for v in historico) / len(historico)
        texto    = "📊 *Últimas partidas:*\n\n" + "\n".join(lineas) + f"\n\n📈 Promedio: {promedio:.0f}%"
    keyboard = [[InlineKeyboardButton("🔄 Jugar de nuevo", callback_data="jugar_nuevo")]]
    await query.edit_message_caption(
        caption=texto,
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )
    return ELEGIR_VERSION


async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎪 *Chavo Bot - Ayuda*\n\n"
        "/start — Iniciar nueva partida\n"
        "/ayuda — Este mensaje\n\n"
        "Elige *Original* o *Animado* y responde 10 preguntas. ¡Fue sin querer queriendo! 😄",
        parse_mode="Markdown",
    )


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ELEGIR_VERSION: [
                CallbackQueryHandler(jugar_nuevo,     pattern="^jugar_nuevo$"),
                CallbackQueryHandler(ver_historial,   pattern="^ver_historial$"),
                CallbackQueryHandler(elegir_version,  pattern="^(original|animado|puntaje_historico)$"),
            ],
            EN_TRIVIA: [
                CallbackQueryHandler(siguiente_pregunta, pattern="^siguiente$"),
                CallbackQueryHandler(responder_pregunta,  pattern="^[0-3]$|^salir$"),
                CallbackQueryHandler(jugar_nuevo,         pattern="^jugar_nuevo$"),
                CallbackQueryHandler(ver_historial,       pattern="^ver_historial$"),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
        per_chat=True,
        per_user=True,
    )

    app.add_handler(conv)
    app.add_handler(CommandHandler("ayuda", ayuda))

    logger.info("🎪 Chavo Bot iniciado... ¡Fue sin querer queriendo! 🛢️")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
