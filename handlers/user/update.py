from loader import bot, tournament

@bot.message_handler(regexp="^Обновить$")
def update(message):
    tournament.update_matches_result()
    tournament.update_forecasts()
    bot.send_message(message.chat.id, "Таблица обновлена")