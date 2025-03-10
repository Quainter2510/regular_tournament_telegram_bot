from loader import bot, tournament
from keyboards.reply.reply_keyboards import get_short_tour_menu_keyboard, get_main_menu_keyboard
from keyboards.inline.inline_keyboards import get_matches_menu
from states.common import MainMenu
from libs.tournament_error import TournamentError

@bot.message_handler(regexp="^Изменить прогноз$")
def choice_tour(message):
    bot.send_message(message.chat.id, "В этом турнире эта функция недоступна")
    return 
    bot.send_message(message.chat.id, "Выберите тур",
                     reply_markup=get_short_tour_menu_keyboard(tournament.get_current_tour()))
    bot.set_state(message.chat.id, MainMenu.choice_tour_for_change_forecast)
    
@bot.message_handler(state=MainMenu.choice_tour_for_change_forecast, regexp=r"^\d{1,} тур")
def choice_match(message):
    tour = int(message.text.split()[0])
    matches = tournament.get_not_started_matches_of_tour(tour)
    bot.send_message(message.chat.id, "Выберите матч",
                     reply_markup=get_matches_menu(matches))
    bot.set_state(message.chat.id, MainMenu.choice_match_for_change_forecast)
    
@bot.callback_query_handler(state=MainMenu.choice_match_for_change_forecast, func=lambda call: call.data != "-1")
def enter_score(call):
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None) 
    bot.edit_message_text(chat_id=call.message.chat.id, 
                          message_id=call.message.message_id,
                          text=call.message.text) 
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data["selected_match_id"] = call.data
    bot.set_state(call.message.chat.id, MainMenu.enter_forecast)
    bot.send_message(call.message.chat.id, "Введите счет")
    
@bot.message_handler(state=MainMenu.enter_forecast, is_correct_score=True, func=lambda call: True)
def set_forecast(message):
    with bot.retrieve_data(message.chat.id, message.chat.id) as data:
        match_id = data.get("selected_match_id")
    try:
        tournament.set_forecast(match_id, message.text, message.chat.id)
        bot.send_message(message.chat.id, "Прогноз изменен", reply_markup=get_main_menu_keyboard())
        bot.set_state(message.chat.id, MainMenu.main_menu)
    except TournamentError as e:
        bot.send_message(message.chat.id, e, reply_markup=get_main_menu_keyboard())
        bot.set_state(message.chat.id, MainMenu.main_menu)
    
@bot.message_handler(state=MainMenu.enter_forecast, is_correct_score=False)
def incorrect_score(message):
    bot.send_message(message.chat.id, "Некорректный счет. Введите два числа через пробел.")