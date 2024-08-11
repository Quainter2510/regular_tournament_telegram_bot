from loader import bot, tournament
from keyboards.reply.reply_keyboards import get_main_menu_keyboard

@bot.message_handler(commands=["fill_forecasts"], is_admin=True)
def fill_forecasts(message):
    tournament.fill_forecasts()
    bot.send_message(message.chat.id, "Прогнозы заполнены", reply_markup=get_main_menu_keyboard())
