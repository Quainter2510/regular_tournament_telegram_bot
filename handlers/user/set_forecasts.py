from loader import bot, tournament
from keyboards.reply.reply_keyboards import get_short_tour_menu_keyboard, get_main_menu_keyboard
from states.common import MainMenu
from libs.tournament_error import TournamentError


@bot.message_handler(state=MainMenu.main_menu, regexp="^Сделать прогноз$")
def choice_tour(message):
    bot.send_message(message.chat.id, "Выберите тур",
                     reply_markup=get_short_tour_menu_keyboard(tournament.get_current_tour()))
    bot.set_state(message.chat.id, MainMenu.choice_tour_for_set_forecast)
    
@bot.message_handler(state=MainMenu.choice_tour_for_set_forecast, regexp=r"^\d{1,} тур")
def choice_match(message):
    tour = int(message.text.split()[0])
    with bot.retrieve_data(message.chat.id, message.chat.id) as data:
        data["selected_tour"] = tour
    matches = tournament.get_not_started_matches_of_tour(tour)
    user_matches = [(match_id, home, away) for match_id, home, away, dt, st in matches]
    if len(matches) == 0:
        bot.send_message(message.chat.id, "Время прогноза истекло", reply_markup=get_main_menu_keyboard())
        bot.set_state(message.chat.id, MainMenu.main_menu)
        return
    bot.send_message(message.chat.id, "Вводите счет через пробел")
    bot.set_state(message.chat.id, MainMenu.set_forecasts)
    match_data = user_matches.pop(0)
    bot.send_message(message.chat.id, f"{match_data[1]}-{match_data[2]}")
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["user_matches"] = user_matches
        data["selected_match_id"] = match_data[0]
        
@bot.message_handler(state=MainMenu.set_forecasts, is_correct_score=True)
def set_forecast(message):
    try:
        with bot.retrieve_data(message.chat.id, message.chat.id) as data:
            match_id = data.get("selected_match_id")
            tournament.set_forecast(match_id, message.text, message.chat.id)
            user_matches = data.get("user_matches")
            if len(user_matches) == 0:
                get_tour_forecasts(message.chat.id)
                bot.set_state(message.chat.id, MainMenu.main_menu)
            else:
                next_match = user_matches.pop(0)
                data["user_matches"] = user_matches
                data["selected_match_id"] = next_match[0]
                bot.send_message(message.chat.id, f"{next_match[1]}-{next_match[2]}")
            
    except TournamentError as e:
        bot.send_message(message.chat.id, e, reply_markup=get_main_menu_keyboard())
        bot.set_state(message.chat.id, MainMenu.main_menu)
        
@bot.message_handler(state=MainMenu.set_forecasts, is_correct_score=False)
def incorrect_score(message):
    bot.send_message(message.chat.id, "Некорректный счет. Введите два числа через пробел.")
        
        
def get_tour_forecasts(user_id):
    with bot.retrieve_data(user_id, user_id) as data:
        tour = data.get("selected_tour")
    matches = tournament.get_matches_of_tour(tour)
    result_info = "Ваш прогноз на {tour} тур :\n\n"
    for match_data in matches:
        predict = tournament.get_predict_match(user_id, match_data[0])
        result_info += f"{match_data[1]} {predict[0]}:{predict[1]} {match_data[2]}\n"
    bot.send_message(user_id, result_info, reply_markup=get_main_menu_keyboard())
    bot.set_state(user_id, MainMenu.main_menu)