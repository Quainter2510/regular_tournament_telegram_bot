from loader import bot, tournament
from keyboards.inline.common import get_all_players_keyboard, get_all_statuses_keyboard
from keyboards.reply.reply_kyeboards import get_main_menu_keyboard
from states.common import Admin, MainMenu
from libs.tournamentError import TournamentError



@bot.message_handler(commands=["set_status"], is_superadmin=True)
def set_status_for_player(message):
    bot.set_state(message.chat.id, Admin.choice_player_for_change_status)
    bot.send_message(message.chat.id, "Выбери пользователя",
                     reply_markup=get_all_players_keyboard(tournament.get_all_players_id_and_usernames()))
    
@bot.callback_query_handler(state=Admin.choice_player_for_change_status, func=lambda call: call.data != "0")
def choice_player_for_change_status(call):
    if tournament.player_is_superadmin(int(call.data)):
        bot.send_message(call.message.chat.id, "Вы не можете изменить статус суперадмина")
        bot.set_state(call.message.chat.id, MainMenu.main_menu)
        return
    bot.send_message(call.message.chat.id, "Выбери статус", reply_markup=get_all_statuses_keyboard(call.data))
    bot.set_state(call.message.chat.id, Admin.change_status)
        
@bot.callback_query_handler(state=Admin.change_status, func=lambda call: call.data != "0")
def change_status_of_player(call):
    player_id, status = call.data.split("_")
    try:
        tournament.set_status_for_player(int(player_id), status)
        bot.send_message(call.message.chat.id, f"Вы изменили статус игрока на {status}",  reply_markup=get_main_menu_keyboard())
    except TournamentError as e:
        bot.send_message(call.message.chat.id, e, reply_markup=get_main_menu_keyboard())
    bot.set_state(call.message.chat.id, MainMenu.main_menu)
    
