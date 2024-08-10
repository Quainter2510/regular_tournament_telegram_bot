import enum
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text


class Base(DeclarativeBase):
    pass


class Match(Base):
    __tablename__ = 'match'

    match_id = Column(Integer, primary_key=True) # from api
    tour = Column(Text, nullable=False)
    status = Column(Text, nullable=False)
    team_home = Column(Text, nullable=False)
    team_away = Column(Text, nullable=False)
    goals_home = Column(Integer)
    goals_away = Column(Integer)
    datetime = Column(DateTime)
    forecast = relationship('Forecast')

    def __repr__(self):
        return (f'Match(id={self.match_id}, tour={self.tour!r}, teams='
                f'{self.team_home!r}-{self.team_away!r})')


class Forecast(Base):
    __tablename__ = 'forecast'

    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey('match.match_id'))
    user_id = Column(Integer, ForeignKey('user.telegram_id'))
    goals_home_predict = Column(Integer)
    goals_away_predict = Column(Integer)
    match_point = Column(Integer)


class User(Base):
    __tablename__ = 'user'

    telegram_id = Column(Integer, primary_key=True, unique=True)
    username = Column(Text, nullable=False, unique=True)
    status = Column(Text, nullable=False)
    payment = Column(Text, nullable=False, default="debtor")
    points_sum = Column(Integer, default=0)
    forecast = relationship('Forecast')
