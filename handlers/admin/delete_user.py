from loader import bot, tournament
from keyboards.inline.inline_keyboards import get_all_players_keyboard
from states.common import Admin, MainMenu
from libs.tournamentError import TournamentError

@bot.message_handler(commands=["delete_user"], is_admin=True)
def providing_choice_for_deletion(message):
    bot.send_message(message.chat.id, "Выберите пользователя",
                     reply_markup=get_all_players_keyboard(tournament.get_all_players_id_and_usernames()))
    bot.set_state(message.chat.id, Admin.choice_player_for_change_delete)
    
@bot.callback_query_handler(state=Admin.choice_player_for_change_delete, func=lambda call: call.data != "0")
def delete_user(call):
    try:
        tournament.delete_player_except_superadmin(int(call.data))
        bot.send_message(call.message.chat.id, "Пользователь был удален")
        bot.send_message(int(call.data), "Вы удалены из турнира")
    except TournamentError as e:
        bot.send_message(call.message.chat.id, e)
    bot.set_state(call.message.chat.id, MainMenu.main_menu)