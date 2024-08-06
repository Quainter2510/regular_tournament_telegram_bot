from loader import bot
from keyboards.inline.common import get_all_players_keyboard
from states.common import Admin, MainMenu


@bot.callback_query_handler(func=lambda call: call.data == "0")
def choice_player_for_change_status(call):
    bot.send_message(call.message.chat.id, "Вы в главном меню")
    bot.set_state(call.message.chat.id, MainMenu.main_menu)