from database.common import DataBase
from config import config
from libs.player import Player
from libs.tournamentError import TournamentError
from libs.parser import Parser

class Tournament:
    def __init__(self) -> None:
        self.database = DataBase()
        self.parser = Parser()

    def add_player(self, nickname, tg_id):
        self.possible_to_register(nickname, tg_id)
        player = Player(nickname, tg_id)
        self.database.add_player(player)
        
    def possible_to_register(self, nickname, tg_id):
        self.throw_already_registered_user_exception(tg_id)
        self.throw_if_name_is_taken_exception(nickname)
        self.throw_registration_closed_exception()
        
    def throw_registration_closed_exception(self):
        if not config.registration_is_open:
            raise TournamentError("Регистрация окончена")
       
    def throw_already_registered_user_exception(self, player_id):
        if self.database.is_repeat_user_in_tournament(player_id):
            raise TournamentError("the player is already registered")
        
    def throw_if_name_is_taken_exception(self, nickname):
        if self.database.is_repeat_nickname_in_tournament(nickname):
            raise TournamentError("the nickname is already registered")

    def player_set_nickname(self, new_nickname, player_id):
        self.database.set_nickname(new_nickname, player_id)
        
    def delete_player_except_superadmin(self, player_id):
        if self.database.player_is_superadmin(player_id):
            raise TournamentError("Этот пользователь не может быть удален")
        self.delete_player(player_id)
        
    def delete_player(self, player_id):
        self.database.delete_player(player_id)
        
    def player_is_admin(self, player_id):
        return self.database.player_is_admin(player_id)
    
    def player_is_superadmin(self, player_id):
        return self.database.player_is_superadmin(player_id)
    
    def set_status_for_player(self, player_id, status):
        self.database.set_status(player_id, status)
        
    def set_payment_for_player(self, player_id, payment):
        self.database.set_payment(player_id, payment) 
        
    def get_all_players_id_and_usernames(self):
        return self.database.get_playersID_and_usernames()
    
    def get_players_info(self):
        return self.database.get_players_info()
    
    def overwrite_matches(self):
        full_matches = self.parser.parse()
        self.database.overwrite_matches(full_matches)
        




        

    
