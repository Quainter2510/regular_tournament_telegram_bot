from telebot import types
from config import config

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

def get_short_tour_menu_keyboard(current_tour):
    marcup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    marcup.add(types.KeyboardButton("Вернуться в меню"))
    min_tour = max(current_tour - 3, 1)
    max_tour = min(current_tour + 3, config.count_tours)
    for i in range(min_tour, max_tour):
        marcup.add(types.KeyboardButton(f"{i} тур"))
    return marcup