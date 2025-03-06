from loader import bot, tournament
from keyboards.inline.inline_keyboards import get_all_settings
from keyboards.reply.reply_keyboards import get_main_menu_keyboard
from states.common import Admin, MainMenu
from libs.tournament_error import TournamentError
from config.config import config



@bot.message_handler(commands=["set_settings"], is_admin=True)
def set_settings(message):
    bot.set_state(message.chat.id, Admin.choice_settings)
    bot.send_message(message.chat.id, "Выбери параметр",
                     reply_markup=get_all_settings())
    
@bot.callback_query_handler(state=Admin.choice_settings, func=lambda call: call.data != "-1")
def choice_settings(call):
    bot.edit_message_text(chat_id=call.message.chat.id, 
                        message_id=call.message.message_id,
                        text=call.message.text)
    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        data["choice_setting"] = call.data
        bot.send_message(call.message.chat.id, f"Текущее значение {config.model_dump()[call.data]}. Напишите новое значение.")
        bot.set_state(call.message.chat.id, Admin.change_settings)
        
@bot.message_handler(state=Admin.change_settings, is_admin=True)
def change_value(message):
    try:
        with bot.retrieve_data(message.chat.id, message.chat.id) as data:
            config.__dict__[data.get('choice_setting')] = define_value(message.text)
            config.save()
            bot.send_message(message.chat.id, "Вы изменили параметр",  reply_markup=get_main_menu_keyboard())
    except TournamentError as e:
        bot.send_message(message.chat.id, e, reply_markup=get_main_menu_keyboard())
    bot.set_state(message.chat.id, MainMenu.main_menu)
    
def define_value(value):
    if value in ["true", "True"]:
        return True 
    elif value in ["False", "false"]:
        return False
    return value