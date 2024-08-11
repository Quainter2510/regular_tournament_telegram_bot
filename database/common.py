from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from typing import List, Tuple
from libs.player import Player
from libs.data_match import DataMatch
from datetime import datetime


from database.models import Base, Match, User, Forecast

def is_admin(id):
    return False

class DataBase:
    def __init__(self):
        engine = create_engine('sqlite:///forecast_bot.db')
        Session = sessionmaker(bind=engine)
        self.session = Session()
        Base.metadata.create_all(engine)

    def add_player(self, player: Player):
        self.add_player_in_database(player)
        self.add_forecasts_for_player(player.id)

    def add_player_in_database(self, player: Player):
        new_user = User(telegram_id=player.id,
                        username=player.nickname,
                        status=player.status,
                        payment=player.payment)
        self.session.add(new_user)
        self.session.commit()

    def add_forecasts_for_player(self, player_id):
        matches_id = self.get_all_matches_id()
        for match_id in matches_id:
            self.add_forecast_for_player(match_id[0], player_id)
    
    def add_match(self, match_data: DataMatch) -> None:
        new_match = Match(match_id=match_data.match_id,
                          tour=match_data.tour,
                          status=match_data.status,
                          team_home=match_data.home_team,
                          team_away=match_data.away_team,
                          goals_home=match_data.home_goals,
                          goals_away=match_data.away_goals,
                          datetime=match_data.datetime)
        self.session.add(new_match)
        self.session.commit()

    def get_all_matches_id(self) -> List[Tuple[int]]:
        """[(match_id,), ...]"""
        return self.session.query(Match.match_id).all()
    
    def add_forecast_for_player(self, match_id, player_id):
        forecast = Forecast(match_id=match_id,
                            user_id=player_id,
                            match_point=0)
        self.session.add(forecast)
        self.session.commit()

    def set_nickname(self, new_nickname, tg_id):
        self.session.query(User).filter(User.telegram_id == tg_id).update({"username": new_nickname})
        self.session.commit()
        
    def set_status(self, tg_id, status):
        self.session.query(User).filter(User.telegram_id == tg_id).update({"status": status})
        self.session.commit()
        
    def set_payment(self, tg_id, payment):
        self.session.query(User).filter(User.telegram_id == tg_id).update({"payment": payment})
        self.session.commit()
        
    def get_playersID_and_usernames(self):
        return self.session.query(User.telegram_id, User.username).all()
    
    def get_players_info(self):
        return self.session.query(User.telegram_id, User.username, User.status, User.payment).all()   
    
    def delete_player(self, player_id):
        self.session.query(User).filter(User.telegram_id == player_id).delete()
        self.session.query(Forecast).filter(Forecast.user_id == player_id).delete()
        self.session.commit()
        
    def player_is_admin(self, player_id):
        return self.session.query(User.status).filter(User.telegram_id == player_id).one_or_none() in [("admin",), ("superadmin",)]
    
    def player_is_superadmin(self, player_id):
        return self.session.query(User.status).filter(User.telegram_id == player_id).one_or_none() == ("superadmin",)
    
    def is_repeat_user_in_tournament(self, player_id):
        return self.session.query(User.telegram_id).filter(User.telegram_id == player_id).one_or_none() != None
    
    def is_repeat_nickname_in_tournament(self, nickname):
        return self.session.query(User.telegram_id).filter(User.username == nickname).one_or_none() != None
    
    def overwrite_matches(self, matches):
        self.session.query(Match).delete()
        for match in matches:
            self.add_match(match)
            
    def get_current_tour(self) -> int:
        cur_tour = self.session.query(Match.tour).filter(Match.datetime > datetime.now()).first()
        if cur_tour == None:
            cur_tour = self.session.query(func.max(Match.tour))
        return int(cur_tour[0])
    
    def get_not_started_matches_of_tour(self, tour):
        '''(match_id, team_home, team_away, datetime, status)'''
        return self.session.query(Match.match_id,
                                  Match.team_home,
                                  Match.team_away,
                                  Match.datetime,
                                  Match.status).filter(Match.tour == tour, 
                                                       Match.datetime > datetime.now()).all()
                                  
    def get_matches_of_tour(self, tour: str):
        '''(match_id, team_home, team_away, datetime, status)'''
        return self.session.query(Match.match_id, Match.team_home, Match.team_away, Match.datetime, Match.status).\
            filter(Match.tour == tour).all()
            
    def set_forecast(self, user_id: int, match_id: int, goals_home_pred: int, goals_away_pred: int) -> None:
        self.session.query(Forecast).filter(Forecast.match_id == match_id,
                                            Forecast.user_id == user_id).\
                                            update({"goals_home_predict": goals_home_pred,
                                                    "goals_away_predict": goals_away_pred})
        self.session.commit()
        
    def is_started_match(self, match_id):
        return self.session.query(Match.match_id).filter(Match.match_id == match_id, 
                                                       Match.datetime > datetime.now()).first() == None
        
    def get_predict_match(self, user_id: int, match_id: int) -> Tuple[int]:
        """(goals_home_predict, goals_away_predict)"""
        return self.session.query(Forecast.goals_home_predict, Forecast.goals_away_predict).\
            filter(Forecast.match_id == match_id, Forecast.user_id == user_id).first()