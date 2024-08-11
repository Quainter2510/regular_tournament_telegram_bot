from loader import bot, tournament
from libs.tournamentError import TournamentError
from telebot.types import Message 
from states.common import Registration, MainMenu
from keyboards.inline.inline_keyboards import *
from telebot.types import CallbackQuery
from sqlalchemy.exc import IntegrityError


@bot.message_handler(commands=["start"])
def start(message: Message):
    try:
        tournament.add_player(f"player{message.chat.id}", message.chat.id)
        bot.set_state(message.chat.id, Registration.confirmation_of_name_change)
        bot.send_message(message.chat.id, f"""Вы зарегистрированы в тернире. Ваше имя player{message.chat.id}. Имя можно менять до начала турнира. Желаете сделать это сейчас?""",
                       reply_markup=confirmation_of_name_change_keyboard())
    except TournamentError as e:
        bot.send_message(message.chat.id, e)
    
@bot.callback_query_handler(func=lambda call: True, state=Registration.confirmation_of_name_change)
def set_nickname(call: CallbackQuery):
    if call.data == "Да":
        bot.send_message(call.from_user.id, "Введите никнейм")
        bot.set_state(call.from_user.id, MainMenu.enter_nickname)
    if call.data == "Нет": 
        bot.send_message(call.from_user.id, "Вы в главном меню")
        bot.set_state(call.from_user.id, Registration.registration)


