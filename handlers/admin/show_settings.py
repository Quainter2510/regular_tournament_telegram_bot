from loader import bot
from config.config import config

@bot.message_handler(commands=["show_settings"], is_admin=True)
def set_payment_for_change_player(message):
    bot.send_message(message.chat.id, config.show())