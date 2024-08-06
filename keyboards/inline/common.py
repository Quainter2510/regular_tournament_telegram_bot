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

def get_all_statuses_keyboard(player_id):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("главное меню", callback_data="0"))
    markup.add(InlineKeyboardButton("admin", callback_data=f"{player_id}_admin"))
    markup.add(InlineKeyboardButton("player", callback_data=f"{player_id}_player"))
    return markup

def get_all_payments_keyboard(player_id):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("главное меню", callback_data="0"))
    markup.add(InlineKeyboardButton("debtor", callback_data=f"{player_id}_debtor"))
    markup.add(InlineKeyboardButton("paid", callback_data=f"{player_id}_paid"))
    return markup
    