from database.common import DataBase
from config.config import config
from libs.player import Player
from libs.tournament_error import TournamentError
from libs.parser import Parser
from libs.logs_handler import LogsHendler

class Tournament:
    def __init__(self) -> None:
        self.database = DataBase()
        self.parser = Parser()
        self.logs_handler = LogsHendler(self.database)

    def add_player(self, nickname, tg_id):
        self.possible_to_register(nickname, tg_id)
        player = Player(nickname, tg_id)
        self.database.add_player(player)
        self.logs_handler.add_player(tg_id)
        
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
        self.logs_handler.player_set_nickname(player_id, new_nickname)
        
    def delete_player_except_superadmin(self, player_id):
        if self.database.player_is_superadmin(player_id):
            raise TournamentError("Этот пользователь не может быть удален")
        self.delete_player(player_id)
        
    def delete_player(self, player_id):
        self.database.delete_player(player_id)
        self.logs_handler.delete_player(player_id)
        
    def player_is_admin(self, player_id):
        return self.database.player_is_admin(player_id)
    
    def player_is_superadmin(self, player_id):
        return self.database.player_is_superadmin(player_id)
    
    def set_status_for_player(self, player_id, status):
        self.database.set_status(player_id, status)
        self.logs_handler.set_status_for_player(player_id, status)
        
    def set_payment_for_player(self, player_id, payment):
        self.database.set_payment(player_id, payment) 
        self.logs_handler.set_payment_for_player(player_id, payment)
        
    def get_all_players_id_and_usernames(self):
        return self.database.get_playersID_and_usernames()
    
    def get_players_info(self):
        return self.database.get_players_info()
    
    def overwrite_matches(self):
        full_matches = self.parser.parse()
        self.database.overwrite_matches(full_matches)
        self.logs_handler.overwrite_matches()
        
    def get_current_tour(self):
        return self.database.get_current_tour()
    
    def get_matches_of_tour(self, tour):
        return self.database.get_matches_of_tour(tour)
        
    def get_not_started_matches_of_tour(self, tour):
        return self.database.get_not_started_matches_of_tour(tour)

    def set_forecast(self, match_id, forecast, player_id):
        if self.database.is_started_match(match_id):
            raise TournamentError("Время прогноза истекло")
        if self.get_predict_match(player_id, match_id) != (None, None):
            self.logs_handler.change_forecast(player_id, match_id, int(forecast.split()[0]), int(forecast.split()[1]))
        else:
            self.logs_handler.set_forecast(player_id, match_id, int(forecast.split()[0]), int(forecast.split()[1]))
        self.database.set_forecast(player_id, match_id, int(forecast.split()[0]), int(forecast.split()[1]))

    def is_started_match(self, match_id):
        return self.database.is_started_match(match_id)

    def get_predict_match(self, player_id, match_id):
        return self.database.get_predict_match(player_id, match_id)
    
    def fill_forecasts(self):
        for player_id, nickname in self.database.get_playersID_and_usernames():
            self.database.add_forecasts_for_player(player_id)
            
    def update_matches_result(self):
        self.database.update_matches_result(self.parser.parse())
        self.logs_handler.update_matches_result()
            
    def update_forecasts(self):
        curr_tour = self.database.get_current_tour()
        self.update_tour(curr_tour)
        self.update_tour(curr_tour - 1)
            
    def counting_of_point_per_match(self, home_goals, away_goals, home_goals_predict, away_goals_predict):        
        if home_goals in ("-", "–", None) or home_goals_predict in ("-", "–", None):
            return 0
        home_goals, away_goals, home_goals_predict, away_goals_predict = map(int, (home_goals,
                                                                                    away_goals,
                                                                                    home_goals_predict,
                                                                                    away_goals_predict))
        if home_goals == home_goals_predict and away_goals == away_goals_predict:
            return 5
        if home_goals - home_goals_predict == away_goals - away_goals_predict:
            return 3
        if home_goals > away_goals and home_goals_predict > home_goals_predict or \
            home_goals < away_goals and home_goals_predict < home_goals_predict:
            return 2
        return 0
    
    def update_tour(self, tour):
        matches = self.database.get_matches_of_tour(tour)
        for match_id, team_home, team_away, datetime, status in matches:
            for player_id, nick in self.database.get_playersID_and_usernames():
                predict = self.database.get_predict_match(player_id, match_id)
                actual = self.database.get_actual_result_match(match_id)
                points_per_match = self.counting_of_point_per_match(*actual, *predict)
                self.database.update_forecast_point(player_id, match_id, points_per_match)
        self.logs_handler.update_tour()
        
    def get_count_of_players(self):
        return self.database.get_count_of_players()
    
    def get_ordered_players_in_intervals(self, start_int, finish_int):
        return self.database.get_ordered_players_in_intervals(start_int, finish_int)
    
    def is_forecast_done(self, tour, player_id):
        return self.database.is_forecast_done(tour, player_id)

    def show_main_table(self, player_id):
        self.logs_handler.get_main_table(player_id)
        
    def show_self_forecast(self, player_id, tour):
        self.logs_handler.get_my_forecast(player_id, tour)
        
    def show_result_tour(self, player_id):
        self.logs_handler.get_result_tour(player_id)
        
    def show_all_other_forecasts(self, player_id, tour):
        self.logs_handler.get_all_other_forecast(player_id, tour)
        
    def show_other_forecasts(self, player_id, tour, subject_id):
        self.logs_handler.get_other_forecast(player_id, tour, subject_id)