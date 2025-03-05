from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text


class LogsBase(DeclarativeBase):
    pass

class HistoryForecast(LogsBase):
    __tablename__ = 'history_forecast'
   
    id = Column(Integer, autoincrement=True, primary_key=True)  
    datetime = Column(DateTime)
    telegram_id = Column(Integer)
    match_id = Column(Integer)
    status = Column(Text)
    goals_home_predict = Column(Integer)
    goals_away_predict = Column(Integer)
    
class HistoryActivities(LogsBase):
    __tablename__ = 'activities'
   
    id = Column(Integer, autoincrement=True, primary_key=True) 
    datetime = Column(DateTime)
    telegram_id = Column(Integer)
    activities = Column(Text, nullable=False)
    description = Column(Text)
     
    