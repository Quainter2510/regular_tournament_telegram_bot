from telebot import types
from config.config import config

def get_main_menu_keyboard() -> types.ReplyKeyboardMarkup:
    marcup = types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=3)
    if config.registration_is_open:
        marcup.add(types.KeyboardButton("Сделать прогноз"),
                #    types.KeyboardButton("Изменить прогноз"),
                types.KeyboardButton("Изменить имя"),
                types.KeyboardButton("Посмотреть итог тура"))
    else:
        marcup.add(types.KeyboardButton("Сделать прогноз"),
                #    types.KeyboardButton("Изменить прогноз"),
                # types.KeyboardButton("Изменить имя"),
                types.KeyboardButton("Посмотреть итог тура"))
    marcup.add(types.KeyboardButton("Посмотреть турнирную таблицу"),
               types.KeyboardButton("Посмотреть свой прогноз"),
               types.KeyboardButton("Обновить"),
               types.KeyboardButton("Вернуться в меню"),
               types.KeyboardButton("Посмотреть прогноз других участников"))
    return marcup

def get_short_tour_menu_keyboard(current_tour):
    marcup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    marcup.add(types.KeyboardButton("Вернуться в меню"))
    min_tour = max(current_tour - 3, config.start_tour)
    max_tour = min(current_tour + 3, config.finish_tour)
    for i in range(min_tour, max_tour):
        marcup.add(types.KeyboardButton(f"{i} тур"))
    return marcup