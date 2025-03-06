from telebot import TeleBot, StateMemoryStorage
from config.config import config
from libs.tournament import Tournament


state_storage = StateMemoryStorage() 
bot = TeleBot(config.MAIN_BOT_TOKEN,
                state_storage=state_storage)

tournament = Tournament()

