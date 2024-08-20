from loader import bot, tournament
from libs.template_creator import TemplateCreator
from config import config
from keyboards.reply.reply_keyboards import get_main_menu_keyboard

@bot.message_handler(commands=["recreate_template"], is_admin=True)
def recreate_template(message):
    number_of_players = max(config.minimum_players, tournament.get_count_of_players())
    template_creator = TemplateCreator(number_of_players,
                                       config.count_tours,
                                       config.count_matches_in_tour)
    template_creator.create_all_templates(config.image_width, config.image_height)
    bot.send_message(message.chat.id, "Шаблоны обновлены", reply_markup=get_main_menu_keyboard())