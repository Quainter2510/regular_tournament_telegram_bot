from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

def confirmation_of_name_change_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Да", callback_data="Да"), 
               InlineKeyboardButton("Нет", callback_data="Нет"))
    return markup

def get_all_players_keyboard(players_data):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("главное меню", callback_data="0"))
    for player_id, username in players_data:
        markup.add(InlineKeyboardButton(username, callback_data=str(player_id)))
    return markup

def get_all_statuses_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("главное меню", callback_data="0"))
    markup.add(InlineKeyboardButton("admin", callback_data="admin"))
    markup.add(InlineKeyboardButton("player", callback_data="player"))
    return markup

def get_all_payments_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("главное меню", callback_data="0"))
    markup.add(InlineKeyboardButton("debtor", callback_data="debtor"))
    markup.add(InlineKeyboardButton("paid", callback_data="paid"))
    return markup
    