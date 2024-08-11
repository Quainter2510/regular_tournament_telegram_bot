from loader import bot, tournament
from keyboards.reply.reply_keyboards import get_main_menu_keyboard

@bot.message_handler(commands=["overwrite"], is_admin=True)
def get_players_info(message):
    tournament.overwrite_matches()
    bot.send_message(message.chat.id, "Матчи перезаписаны", reply_markup=get_main_menu_keyboard())