from loader import bot, tournament
from states.common import Admin, MainMenu

@bot.message_handler(commands=["send_all"], is_admin=True)
def enter_message_for_all(message):
    bot.send_message(message.chat.id, "Введите сообщение, которое будет разослано всем игрокам")
    bot.set_state(message.chat.id, Admin.send_all)
    
@bot.message_handler(state=Admin.send_all, is_admin=True)
def send_all(message):
    players_id_and_usernames = tournament.get_all_players_id_and_usernames()
    for id, name in players_id_and_usernames:
        bot.send_message(id, message.text)
    bot.set_state(message.chat.id, MainMenu.main_menu)