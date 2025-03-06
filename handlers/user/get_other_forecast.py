from loader import bot, tournament
from config.config import config
from image_fillers.points_tour_filler import PointsTourFiller
from image_fillers.result_tour_filler import ResultTourFiller
from keyboards.reply.reply_keyboards import get_main_menu_keyboard, get_short_tour_menu_keyboard
from keyboards.inline.inline_keyboards import get_player_or_all
from states.common import MainMenu

@bot.message_handler(regexp="^Посмотреть прогноз других участников$")
def choice_tour(message):
    bot.send_message(message.chat.id, "Выберите тур",
                     reply_markup=get_short_tour_menu_keyboard(tournament.get_current_tour()))
    bot.set_state(message.chat.id, MainMenu.choice_tour_for_send_forecast)
    
@bot.message_handler(state=MainMenu.choice_tour_for_send_forecast, regexp=r"^\d{1,} тур")
def get_result_tour(message):
    tour = int(message.text.split()[0]) 
    if not tournament.is_forecast_done(tour, message.chat.id):
        bot.send_message(message.chat.id, "Вы не можете смотреть прогнозы других игроков пока не сделаете прогноз",
                         reply_markup=get_main_menu_keyboard())
        bot.set_state(message.chat.id, MainMenu.main_menu)
        return 
    bot.send_message(message.chat.id, "Выберите игрока", reply_markup=get_player_or_all(tournament.get_all_players_id_and_usernames()))
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["selected_tour"] = tour 
    bot.set_state(message.chat.id, MainMenu.choice_players_forecast)

@bot.callback_query_handler(state=MainMenu.choice_players_forecast, func=lambda call: call.data != "-1")
def send_forecast(call):
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None) 
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        tour = data.get("selected_tour")
    if call.data == "all":
        players = tournament.get_ordered_players_in_intervals(0, tour)
        tournament.show_all_other_forecasts(call.message.chat.id, tour)
        for nick, player_id, points in players:
            send_player_forecast(tour, player_id, call.from_user.id)
    else:
        user_id = int(call.data)
        send_player_forecast(tour, user_id, call.from_user.id)
        
def send_player_forecast(tour, player_id, chat_id):
    result_filler = ResultTourFiller(tournament.database,
                                     config.count_matches_in_tour, 
                                     config.image_width,
                                     config.image_height)
    result_filler.fill_table(tour, player_id)
    img = open("images/ready_tables/result_tour.png", 'rb')
    bot.send_photo(chat_id, img, reply_markup=get_main_menu_keyboard())
    