from loader import bot, tournament
from states.common import MainMenu
from keyboards.reply.reply_keyboards import get_main_menu_keyboard
from sqlalchemy.exc import IntegrityError
from libs.tournament_error import TournamentError


@bot.message_handler(state="*", regexp="^Изменить имя$")
def set_nickname(message):
    bot.set_state(message.chat.id, MainMenu.enter_nickname)
    bot.send_message(message.chat.id, "Введите новое имя")

@bot.message_handler(state=MainMenu.enter_nickname)
def set_nickname(message):
    try:
        tournament.player_set_nickname(message.text, message.chat.id)
        bot.set_state(message.chat.id, MainMenu.main_menu)
        bot.send_message(message.chat.id, f"Имя изменено на {message.text}", reply_markup=get_main_menu_keyboard())
        bot.send_message(message.chat.id, "Вы в главном меню", reply_markup=get_main_menu_keyboard())
    except TournamentError as e:
        bot.send_message(message.chat.id, e)
    except IntegrityError:
        bot.send_message(message.chat.id, "Это имя занято")