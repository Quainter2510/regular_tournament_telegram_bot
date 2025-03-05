from sqlalchemy import create_engine, func, desc
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from database.logs_models import LogsBase, HistoryActivities, HistoryForecast

class DataBase:
    def __init__(self):
        engine = create_engine('sqlite:///bot_logs.db')
        Session = sessionmaker(bind=engine)
        self.session = Session()
        LogsBase.metadata.create_all(engine)
        
    def add_to_forecast_history(self, forecast_data):
        history_forecast = HistoryForecast(datetime=datetime.now(),
                                           telegram_id=forecast_data.player_id,
                                           match_id=forecast_data.match_id,
                                           status=forecast_data.status,
                                           goals_home_predict=forecast_data.home_goals,
                                           goals_away_predict=forecast_data.away_goals)
        self.session.add(history_forecast)
        self.session.commit()
        
    def add_to_activities_history(self, activities_data):
        activities_history = HistoryActivities(datetime=datetime.now(),
                                               telegram_id=activities_data.player_id,
                                               activities=activities_data.activities,
                                               description=activities_data.description)
        self.session.add(activities_history)
        self.session.commit()
        
    