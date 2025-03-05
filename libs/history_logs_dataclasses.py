from dataclasses import dataclass
    
@dataclass
class ForecastLogsData:
    player_id: int
    match_id: int
    status: str
    home_goals: str
    away_goals: str
    
@dataclass
class ActivitiesLogsData:
    player_id: int
    activities: str
    description: str 