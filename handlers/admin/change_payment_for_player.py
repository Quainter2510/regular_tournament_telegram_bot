from loader import bot, tournament
from keyboards.inline.inline_keyboards import get_all_players_keyboard, get_all_payments_keyboard
from keyboards.reply.reply_keyboards import get_main_menu_keyboard
from states.common import Admin, MainMenu
from libs.tournament_error import TournamentError



@bot.message_handler(commands=["set_payment"], is_admin=True)
def set_payment_for_change_player(message):
    bot.set_state(message.chat.id, Admin.choice_player_for_change_payment)
    bot.send_message(message.chat.id, "Выбери пользователя",
                     reply_markup=get_all_players_keyboard(tournament.get_all_players_id_and_usernames()))
    
@bot.callback_query_handler(state=Admin.choice_player_for_change_payment, func=lambda call: call.data != "-1")
def choice_player_for_change_payment(call):
    bot.edit_message_text(chat_id=call.message.chat.id, 
                        message_id=call.message.message_id,
                        text=call.message.text)
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data["choice_player"] = call.data
        bot.send_message(call.message.chat.id, "Выбери статус оплаты", reply_markup=get_all_payments_keyboard())
        bot.set_state(call.message.chat.id, Admin.change_payment)
        
@bot.callback_query_handler(state=Admin.change_payment, func=lambda call: call.data != "-1")
def change_payment_of_player(call):
    bot.edit_message_text(chat_id=call.message.chat.id, 
                        message_id=call.message.message_id,
                        text=call.message.text)
    try:
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            tournament.set_payment_for_player(int(data.get("choice_player")), call.data)
            bot.send_message(call.message.chat.id, "Вы изменили статус оплаты игрока",  reply_markup=get_main_menu_keyboard())
    except TournamentError as e:
        bot.send_message(call.message.chat.id, e, reply_markup=get_main_menu_keyboard())
    bot.set_state(call.message.chat.id, MainMenu.main_menu)
    
