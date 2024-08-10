from telebot.handler_backends import State, StatesGroup
from loader import bot
from telebot import custom_filters
from libs.additional_filters import *


class Registration(StatesGroup):
    registration = State()
    confirmation_of_name_change = State()
    

class MainMenu(StatesGroup):
    main_menu = State()
    enter_nickname = State()
    

class Admin(StatesGroup):
    choice_player_for_change_status = State()
    change_status = State()
    
    choice_player_for_change_payment = State()
    change_payment = State()  
    
    choice_player_for_change_delete = State()
    
    send_all = State()
     
    


bot.add_custom_filter(custom_filters.StateFilter(bot))
