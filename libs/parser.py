from re import fullmatch
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from libs.data_match import DataMatch
from config import config



class Parser:   
    def time_transform(self, datetime: str) -> str:
        time = " ".join(datetime.split()[1:])
        time = "00:00" if time == 'ок' else time
        return time 
    
    def get_match_status(self, datetime: str) -> str:
        time = datetime.split()[1]
        if time == "ок":
            return "finished"
        if fullmatch(r"\d\d:\d\d", time):
            return "expected"
        return "in process"

    def parse(self):
        response = requests.get(config.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        quotes = soup.find('div', class_="cal_sort_tour").find_all("div")
        res = []
        for i, quote in enumerate(quotes):
            match_id = i
            tour = i // config.count_matches_in_tour + 1
            dt = quote.find_all("li")[0].text
            status = self.get_match_status(dt)
            date = dt.split()[0]
            time = self.time_transform(dt)
            dt = datetime.strptime(f"{date} {time}", "%d/%m/%Y %H:%M")
            commands = quote.find_all("li")[1].find_all("span")
            home_team = commands[0].text.replace("*", "").strip()
            away_team = commands[1].text.replace("*", "").strip()
            result = quote.find_all("a")[0].text.split(":")
            home_team_goals = result[0]
            away_team_goals = result[1]
            if config.start_tour <= tour <= config.finish_tour:
                res.append(DataMatch(match_id=match_id,
                                    tour=tour,
                                    datetime=dt,
                                    status=status,
                                    home_team=home_team,
                                    away_team=away_team,
                                    home_goals=home_team_goals,
                                    away_goals=away_team_goals))
        return res