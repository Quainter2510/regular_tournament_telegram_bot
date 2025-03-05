from loader import bot, tournament
from config import config
from image_fillers.points_tour_filler import PointsTourFiller
from image_fillers.result_tour_filler import ResultTourFiller
from keyboards.reply.reply_keyboards import get_main_menu_keyboard, get_short_tour_menu_keyboard
from states.common import MainMenu

@bot.message_handler(regexp="^Посмотреть итог тура$")
def choice_tour(message):
    bot.send_message(message.chat.id, "Выберите тур",
                     reply_markup=get_short_tour_menu_keyboard(tournament.get_current_tour()))
    bot.set_state(message.chat.id, MainMenu.choice_tour_for_check_result)
    
@bot.message_handler(state=MainMenu.choice_tour_for_check_result, regexp=r"^\d{1,} тур")
def get_result_tour(message):
    tour = int(message.text.split()[0])
    points_filler = PointsTourFiller(tournament.database, 
                                   max(tournament.get_count_of_players(), config.minimum_players),
                                   config.image_width,
                                   config.image_height)
    points_filler.fill_table(tour)
    img = open("images/ready_tables/points_tour.png", 'rb')
    bot.send_photo(message.chat.id, img)  
    
    result_filler = ResultTourFiller(tournament.database,
                                     config.count_matches_in_tour, 
                                     config.image_width,
                                     config.image_height)
    result_filler.fill_table(tour, message.chat.id)
    img = open("images/ready_tables/result_tour.png", 'rb')
    bot.send_photo(message.chat.id, img, reply_markup=get_main_menu_keyboard())
    tournament.show_result_tour(message.chat.id)
      