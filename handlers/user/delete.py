from loader import bot, tournament

@bot.message_handler(commands=["delete"])
def delete(message):
    tournament.delete_player(message.chat.id)
    bot.send_message(message.chat.id, "Вы удалены")
    
    