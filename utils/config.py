from environs import Env

# Инициализация environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")

REDIS_HOST = env.str("REDIS_HOST")
REDIS_PORT = env.int("REDIS_PORT")

# Конфигурация базы данных
# DB_CONFIG = {
#     "host": env.str("DB_HOST"),
#     "port": env.int("DB_PORT"),
#     "dbname": env.str("DB_NAME"),
#     "user": env.str("DB_USER"),
#     "password": env.str("DB_PASSWORD")
# }
DB_URL = env.str("DB_URL")

USE_PROXY = env.bool("USE_PROXY", False)
HTTP_PROXY = env.str("HTTP_PROXY", None)
PROXY_CONFIG = {
    "proxy": HTTP_PROXY if USE_PROXY else None
}
