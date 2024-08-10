from dataclasses import dataclass
from datetime import datetime

@dataclass
class DataMatch:
    match_id: int
    tour: int
    datetime: datetime
    status: str
    home_team: str
    away_team: str
    home_goals: str
    away_goals: str