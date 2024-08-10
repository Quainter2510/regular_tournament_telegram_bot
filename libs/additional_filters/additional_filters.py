import telebot
from loader import tournament, bot

class IsAdmin(telebot.custom_filters.SimpleCustomFilter):
    key='is_admin'
    @staticmethod
    def check(message: telebot.types.Message):
        return tournament.player_is_admin(message.chat.id)
    
    
class IsSuperadmin(telebot.custom_filters.SimpleCustomFilter):
    key='is_superadmin'
    @staticmethod
    def check(message: telebot.types.Message):
        return tournament.player_is_superadmin(message.chat.id)
    
    
    

bot.add_custom_filter(IsAdmin())
bot.add_custom_filter(IsSuperadmin())