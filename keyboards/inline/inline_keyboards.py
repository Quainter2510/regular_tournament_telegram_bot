from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

def confirmation_of_name_change_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Да", callback_data="Да"), 
               InlineKeyboardButton("Нет", callback_data="Нет"))
    return markup

def get_all_players_keyboard(players_data):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("главное меню", callback_data="-1"))
    for player_id, username in players_data:
        markup.add(InlineKeyboardButton(username, callback_data=str(player_id)))
    return markup

def get_player_or_all(players_data):
    markup = get_all_players_keyboard(players_data)
    markup.add(InlineKeyboardButton("Выбрать всех", callback_data="all"))
    return markup

def get_all_statuses_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("главное меню", callback_data="-1"))
    markup.add(InlineKeyboardButton("admin", callback_data="admin"))
    markup.add(InlineKeyboardButton("player", callback_data="player"))
    return markup

def get_all_payments_keyboard():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("главное меню", callback_data="-1"))
    markup.add(InlineKeyboardButton("debtor", callback_data="debtor"))
    markup.add(InlineKeyboardButton("paid", callback_data="paid"))
    return markup
    
def get_matches_menu(matches):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("главное меню", callback_data="-1"))
    for match_id, team_home, team_away, datetime, status in matches:
        markup.add(InlineKeyboardButton(f"{team_home}-{team_away}", callback_data=str(match_id)))
    return markup

def get_all_settings():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("all_func_ready", callback_data="all_func_ready"))
    markup.add(InlineKeyboardButton("registration_is_open", callback_data="registration_is_open"))
    markup.add(InlineKeyboardButton("count_matches_in_tour", callback_data="count_matches_in_tour"))
    markup.add(InlineKeyboardButton("count_tours", callback_data="count_tours"))
    markup.add(InlineKeyboardButton("start_tour", callback_data="start_tour"))
    markup.add(InlineKeyboardButton("finish_tour", callback_data="finish_tour"))
    markup.add(InlineKeyboardButton("главное меню", callback_data="-1"))
    return markup