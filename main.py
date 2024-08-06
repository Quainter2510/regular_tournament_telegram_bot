from loader import bot
import handlers


# if __name__ == '__main__':
#     while True:
#         try:
#             bot.polling(none_stop=True)
#         except Exception as exc:
#             bot.send_message(config.ADMIN_ID, exc, reply_markup=my_marcup.main_menu_marcup())
# 

bot.polling(non_stop=True)