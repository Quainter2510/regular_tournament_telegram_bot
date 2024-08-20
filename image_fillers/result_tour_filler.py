from libs.markup_table import Result_tour_markup
from database.common import Base
from image_fillers.image_filler import ImageFiller

class ResultTourFiller(ImageFiller):
    def __init__(self, database: Base, count_matches_in_tour, width, height) -> None:
        super().__init__(database, width, height, "result_tour")
        self.markup = Result_tour_markup(self.width, self.height, count_matches_in_tour)
        
    def fill_table(self, tour, player_id):
        self.create_imagedraw()
        matches = self.database.get_matches_of_tour(tour)
        nickname = self.database.get_nickname(player_id)
        self.fill_head(tour, nickname)
        for row, (match_id, team_home, team_away, datetime, status) in enumerate(matches, start=1):
            self.fill_row(row, player_id, match_id)
        result_points = self.database.get_main_points_per_tour(player_id, tour)
        self.fill_result_points(result_points)
        self.save_image()
        
    def fill_row(self, row, player_id, match_id):
        commands = self.database.get_commands(match_id)
        actual_score = self.database.get_actual_result_match(match_id)
        predict_score = self.database.get_predict_match(player_id, match_id)
        points = self.database.get_points_of_match(player_id, match_id)       
        self.fill_command_name(row, *commands)
        self.fill_actual_score(row, *actual_score)
        self.fill_predict_score(row, *predict_score)
        self.fill_points(row, points)

    def fill_head(self, tour, nickname):
        self.drawtext(self.imdraw, 0, 0, self.markup.image_width, self.markup.head_size, f'Прогноз на {tour} тур от {nickname}')
    
    def fill_command_name(self, row, home_team, away_team):
        self.drawtext(self.imdraw,
                      self.markup.match_size["x"], self.markup.head_size + self.markup.dy * row,
                      self.markup.match_size["dx"], self.markup.dy, f"{home_team}-{away_team}")
        
    def fill_actual_score(self, row, home_team_goals, away_team_goals):
        self.drawtext(self.imdraw, self.markup.result_size["x"], self.markup.head_size + self.markup.dy * row,
                      self.markup.result_size["dx"], self.markup.dy, f"{home_team_goals}:{away_team_goals}")
        
    def fill_predict_score(self, row, home_team_predict, away_team_predict):
        self.drawtext(self.imdraw, self.markup.forecast_size["x"], self.markup.head_size + self.markup.dy * row,
                      self.markup.forecast_size["dx"], self.markup.dy, f"{home_team_predict}:{away_team_predict}")  
    
    def fill_points(self, row, points):
        self.drawtext(self.imdraw, self.markup.points_size["x"], self.markup.head_size + self.markup.dy * row,
                      self.markup.points_size["dx"], self.markup.dy, f"{points}")     
        
    def fill_result_points(self, result_points):
          self.drawtext(self.imdraw,
                        self.markup.points_size["x"],
                        self.markup.image_height - self.markup.total_size,
                        self.markup.points_size["dx"],
                        self.markup.total_size,
                        str(result_points))
    
        
        