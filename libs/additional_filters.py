import telebot
from loader import tournament, bot
from re import fullmatch

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
    
    
class IsCorrectScore(telebot.custom_filters.SimpleCustomFilter):
    key='is_correct_score'
    @staticmethod
    def check(message: telebot.types.Message):
        return fullmatch(r"\d{1,} \d{1,}", message.text) != None
    
    

bot.add_custom_filter(IsAdmin())
bot.add_custom_filter(IsSuperadmin())
bot.add_custom_filter(IsCorrectScore())