from loader import bot, tournament
from keyboards.reply.reply_keyboards import get_main_menu_keyboard
from states.common import MainMenu
from keyboards.reply.reply_keyboards import get_short_tour_menu_keyboard, get_main_menu_keyboard 

@bot.message_handler(regexp="^Посмотреть свой прогноз$")
def choice_tour(message):
    bot.send_message(message.chat.id, "Выберите тур",
                     reply_markup=get_short_tour_menu_keyboard(tournament.get_current_tour()))
    bot.set_state(message.chat.id, MainMenu.choice_tour_for_check_self_forecast)
    
    
    
@bot.message_handler(state=MainMenu.choice_tour_for_check_self_forecast, regexp=r"^\d{1,} тур")   
def get_tour_forecasts(message):
    tour = int(message.text.split()[0])
    matches = tournament.get_matches_of_tour(tour)
    result_info = f"Ваш прогноз на {tour} тур :\n\n"
    for match_data in matches:
        predict = tournament.get_predict_match(message.chat.id, match_data[0])
        result_info += f"{match_data[1]} {predict[0]}:{predict[1]} {match_data[2]}\n"
    bot.send_message(message.chat.id, result_info, reply_markup=get_main_menu_keyboard())
    tournament.show_self_forecast(message.chat.id)
    bot.set_state(message.chat.id, MainMenu.main_menu)