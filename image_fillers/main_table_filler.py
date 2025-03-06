from libs.markup_table import Main_table_markup, Points_tour_markup, Result_tour_markup
from PIL import ImageDraw, ImageFont, Image
from config.config import config
from database.common import Base
from image_fillers.image_filler import ImageFiller

class MainTableFiller(ImageFiller):
    def __init__(self, database: Base, number_of_player, width, height, count_of_tour) -> None:
        super().__init__(database, width, height, "main_table")
        self.count_of_tour = count_of_tour
        self.markup = Main_table_markup(self.width, self.height, number_of_player, count_of_tour)
        
    def fill_table(self):
        self.create_imagedraw()
        current_tour = self.database.get_current_tour()
        players = self.database.get_ordered_players_in_intervals(0, current_tour)
        for row, (nick, player_id, points) in enumerate(players):
            self.fill_row(row, player_id)
        self.save_image()
        
    def fill_row(self, row, player_id):
        current_tour = self.database.get_current_tour()
        nickname = self.database.get_nickname(player_id)
        sum_points = self.database.get_sum_points_of_player(player_id)
        self.fill_name(row, nickname)
        for tour in range(config.start_tour, config.finish_tour + 1):
            points = self.database.get_main_points_per_tour(player_id, tour)
            if tour > current_tour + 1:
                points = "-"
            self.fill_points(row, tour - config.start_tour, str(points))
        self.fill_sum_points(row, str(sum_points))
        
    def fill_name(self, row, nickname):
        self.drawtext(self.imdraw,
                      self.markup.name_size["x"], self.markup.head_size + self.markup.dy * row,
                      self.markup.name_size["dx"], self.markup.dy, nickname)
        
    def fill_points(self, row, col, points):
        self.drawtext(self.imdraw,
                      self.markup.tours_size["x"] + self.markup.tours_dx * col,
                      self.markup.head_size + self.markup.dy * row,
                      self.markup.tours_dx, self.markup.dy,
                      points)
        
    def fill_sum_points(self, row, points):
        self.drawtext(self.imdraw,
                      self.markup.sum_size["x"],
                      self.markup.head_size + self.markup.dy * row,
                      self.markup.sum_size["dx"],
                      self.markup.dy,
                      points)
       
    
        
        