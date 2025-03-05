from database.logs_database import DataBase
from libs.history_logs_dataclasses import ActivitiesLogsData, ForecastLogsData

class LogsHendler:
    def __init__(self):
        self.database = DataBase()
        
    def change_forecast(self, player_id, match_id, goals_home, goals_away):
        foreacast_data = ForecastLogsData(player_id, 
                                          match_id,
                                          "change", 
                                          goals_home,
                                          goals_away)
        self.database.add_to_forecast_history(foreacast_data)
        
    def set_forecast(self, player_id, match_id, goals_home, goals_away):
        foreacast_data = ForecastLogsData(player_id, 
                                          match_id,
                                          "set", 
                                          goals_home,
                                          goals_away)
        self.database.add_to_forecast_history(foreacast_data)
        
    def delete_player(self, player_id):
        activities_data = ActivitiesLogsData(player_id,
                                             "delete player",
                                             f"")
        self.database.add_to_activities_history(activities_data)
        
    def get_main_table(self, player_id):
        activities_data = ActivitiesLogsData(player_id,
                                             "get main table",
                                             "")
        self.database.add_to_activities_history(activities_data)
        
    def get_result_tour(self, player_id):
        activities_data = ActivitiesLogsData(player_id,
                                             "get result tour",
                                             "")
        self.database.add_to_activities_history(activities_data)
        
    def get_my_forecast(self, player_id, tour):
        activities_data = ActivitiesLogsData(player_id,
                                             "get self forecast",
                                             f"get self forecast for {tour} tour")
        self.database.add_to_activities_history(activities_data)
        
    def get_all_other_forecast(self, player_id, tour):
        activities_data = ActivitiesLogsData(player_id,
                                             "get all other forecast",
                                             f"get all other forecast for {tour} tour")
        self.database.add_to_activities_history(activities_data)
        
    def get_other_forecast(self, player_id, tour, subject_id):
        activities_data = ActivitiesLogsData(player_id,
                                             "get other forecast",
                                             f"get other forecast for {tour} tour of player {subject_id}")
        self.database.add_to_activities_history(activities_data)
        
    def add_player(self, player_id):
        activities_data = ActivitiesLogsData(player_id,
                                             "player registred",
                                             f"")
        self.database.add_to_activities_history(activities_data)  
        
    def player_set_nickname(self, player_id, nickname):
        activities_data = ActivitiesLogsData(player_id,
                                             "player set nickname",
                                             f"player set nickname {nickname}")
        self.database.add_to_activities_history(activities_data)       
        
    def set_status_for_player(self, player_id, status):
        activities_data = ActivitiesLogsData(player_id,
                                             "change status for player",
                                             f"player set status {status}")
        self.database.add_to_activities_history(activities_data)
        
    def set_payment_for_player(self, player_id, status):
        activities_data = ActivitiesLogsData(player_id,
                                             "change payment for player",
                                             f"player set payment status {status}")
        self.database.add_to_activities_history(activities_data)
        
    def overwrite_matches(self):
        activities_data = ActivitiesLogsData(0,
                                             "overwrite matches",
                                             f"")
        self.database.add_to_activities_history(activities_data)
        
    def update_matches_result(self):
        activities_data = ActivitiesLogsData(0,
                                             "update matches result",
                                             f"")
        self.database.add_to_activities_history(activities_data)
        
    def update_tour(self):
        activities_data = ActivitiesLogsData(0,
                                             "update tour",
                                             f"")
        self.database.add_to_activities_history(activities_data)