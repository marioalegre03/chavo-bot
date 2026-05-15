# 🎪 Chavo Bot — Trivia del Chavo del Ocho

> Bot de Telegram con trivia interactiva del Chavo del Ocho.  
> Elige entre la versión **📺 Original (1971)** o la **🎨 Animada (2006)** y responde 10 preguntas aleatorias.

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://python.org)
[![python-telegram-bot](https://img.shields.io/badge/python--telegram--bot-20.8-blue)](https://python-telegram-bot.org)
[![Deploy on Fly.io](https://img.shields.io/badge/Deploy-Fly.io-purple?logo=fly)](https://fly.io)
[![Deploy on Render](https://img.shields.io/badge/Deploy-Render-green?logo=render)](https://render.com)

---

## 🚀 Instalación local

```bash
# 1. Clonar el repo
git clone https://github.com/luisitoys12/chavo-bot.git
cd chavo-bot

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Crear el archivo .env
cp .env.example .env
# Edita .env y pega tu token de @BotFather

# 4. Ejecutar
export BOT_TOKEN=tu_token_aqui
python bot.py
```

---

## 🔑 Obtener el token

1. Abre Telegram y busca **@BotFather**
2. Envía `/newbot`
3. Ponle el nombre: **Chavo Bot** y el username: `@chavo_trivia_bot` (o el que esté libre)
4. Copia el token que te da

---

## ☁️ Deploy en producción

### Fly.io (recomendado)

```bash
# Instalar flyctl si no lo tienes
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Deploy
fly launch          # la primera vez
fly secrets set BOT_TOKEN=tu_token_aqui
fly deploy
```

### Render.com

1. Crea un nuevo servicio tipo **Background Worker**
2. Conecta este repositorio de GitHub
3. Build command: `pip install -r requirements.txt`
4. Start command: `python bot.py`
5. En **Environment Variables** agrega: `BOT_TOKEN = tu_token_aqui`
6. ¡Deploy!

---

## 🎮 Comandos del bot

| Comando | Descripción |
|---------|-------------|
| `/start` | Inicia una nueva partida |
| `/ayuda` | Muestra la ayuda |

---

## 📋 Características

- ✅ **30 preguntas** en total (15 por versión)
- ✅ **10 preguntas aleatorias** por partida
- ✅ Imágenes en bienvenida, versión y resultado
- ✅ Datos curiosos tras cada respuesta
- ✅ Historial y promedio de partidas por usuario
- ✅ Botones inline con teclado interactivo
- ✅ Sistema de puntaje con calificaciones
- ✅ Token leído de variable de entorno (seguro para producción)

---

## 🗂️ Estructura

```
chavo-bot/
├── bot.py            # Código principal del bot
├── requirements.txt  # Dependencias
├── Dockerfile        # Para deploy con Docker
├── fly.toml          # Configuración Fly.io
├── render.yaml       # Configuración Render
├── .env.example      # Plantilla de variables de entorno
├── .gitignore        # Archivos ignorados por git
└── README.md         # Esta documentación
```

---

## ⚙️ Variables de entorno

| Variable | Descripción | Requerida |
|----------|-------------|----------|
| `BOT_TOKEN` | Token de tu bot de Telegram (@BotFather) | ✅ Sí |

---

## 🧑‍💻 Autor

**Luis Martinez** — [Estacionkusmedios](https://estacionkusmedios.org)  
Irapuato, Guanajuato, México 🇲🇽

---

*¡Fue sin querer queriendo!* 🛢️
