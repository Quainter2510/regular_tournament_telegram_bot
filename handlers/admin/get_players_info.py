from loader import bot, tournament

@bot.message_handler(commands=["get_players_info"], is_admin=True)
def get_players_info(message):
    players_info = tournament.get_players_info()
    info_msg = ""
    for id, name, status, payment in players_info:
        info_msg += f"{id} {name} {status} {payment}\n"
    bot.send_message(message.chat.id, info_msg)