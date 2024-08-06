from telebot import types


def get_main_menu_keyboard() -> types.ReplyKeyboardMarkup:
    marcup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    marcup.add(types.KeyboardButton("Сделать прогноз"),
               types.KeyboardButton("Изменить прогноз"),
               types.KeyboardButton("Изменить имя"),
               types.KeyboardButton("Посмотреть итог тура"),
               types.KeyboardButton("Посмотреть турнирную таблицу"),
               types.KeyboardButton("Посмотреть свой прогноз"),
               types.KeyboardButton("Обновить"),
               types.KeyboardButton("Сброс"),
               types.KeyboardButton("Посмотреть прогноз всех участников"))
    return marcup