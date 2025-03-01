from loader import bot
from config import config
from keyboards.reply.reply_keyboards import get_main_menu_keyboard
import handlers


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as exc:
            bot.send_message(config.ADMIN_ID, exc, reply_markup=get_main_menu_keyboard())


# bot.polling(non_stop=True)