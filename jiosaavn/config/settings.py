from os import getenv

API_ID = getenv("API_ID", "26267563")
API_HASH = getenv("API_HASH", "6665b1e3a30bb824973bf1b8b1603bb9")
BOT_TOKEN = getenv("BOT_TOKEN", "6381141611:AAGJM15_TQAQg6YezcPswigPukDJf1Czfyg")
BOT_COMMANDS = (
    ("start", "Initialize the bot and check its status"),
    ("settings", "Configure and manage bot settings"),
    ("help", "Get information on how to use the bot"),
    ("about", "Learn more about the bot and its features"),
)

DATABASE_URL = getenv("DATABASE_URL", "mongodb+srv://vasudurainc:vasudurainc123@cluster01.2bypjge.mongodb.net/?retryWrites=true&w=majority")
HOST = getenv("HOST", "0.0.0.0")
PORT = int(getenv("PORT", "8080"))
