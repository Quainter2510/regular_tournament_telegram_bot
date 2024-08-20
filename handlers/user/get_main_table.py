from loader import bot, tournament
from config import config
from keyboards.reply.reply_keyboards import get_main_menu_keyboard
from image_fillers.main_table_filler import MainTableFiller

@bot.message_handler(regexp="^Посмотреть турнирную таблицу$")
def get_main_table(message):
    result_filler = MainTableFiller(tournament.database,
                                     config.count_matches_in_tour, 
                                     config.image_width,
                                     config.image_height,
                                     config.count_tours)
    result_filler.fill_table()
    img = open("images/ready_tables/main_table.png", 'rb')
    bot.send_photo(message.chat.id, img, reply_markup=get_main_menu_keyboard())