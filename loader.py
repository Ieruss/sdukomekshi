from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from utils.config import load_config, Config
from database.engine import Database

config: Config = load_config()
bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
db: Database = Database()