from loader import bot
from states.common import MainMenu
from keyboards.reply.reply_keyboards import get_main_menu_keyboard


@bot.callback_query_handler(func=lambda call: call.data == "-1")
def home_from_call(call):
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None) 
    bot.send_message(call.message.chat.id, "Вы в главном меню", reply_markup=get_main_menu_keyboard())
    bot.set_state(call.message.chat.id, MainMenu.main_menu)
    
@bot.message_handler(regexp="^Вернуться в меню$")
def home_from_message(message):
    bot.send_message(message.chat.id, "Вы в главном меню", reply_markup=get_main_menu_keyboard())
    bot.set_state(message.chat.id, MainMenu.main_menu)