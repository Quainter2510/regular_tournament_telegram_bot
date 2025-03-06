from libs.markup_table import Main_table_markup, Points_tour_markup, Result_tour_markup
from PIL import ImageDraw, ImageFont, Image
from config.config import config
from database.common import Base
from image_fillers.image_filler import ImageFiller

class PointsTourFiller(ImageFiller):
    def __init__(self, database: Base, number_of_player, width, height) -> None:
        super().__init__(database, width, height, "points_tour")
        self.markup = Points_tour_markup(number_of_player, self.width, self.height)
        
    def fill_table(self, tour):
        self.create_imagedraw()
        players = self.database.get_ordered_players_in_intervals(0, tour)
        for row, (nick, player_id, points) in enumerate(players, start=1):
            self.fill_row(row, player_id, tour)
        self.save_image()
        
    def fill_row(self, row, player_id, tour):
        nick = self.database.get_nickname(player_id)
        points = self.database.get_main_points_per_tour(player_id, tour)
        additional_points = self.database.get_additional_points_per_tour(player_id, tour)
        self.fill_name(row, nick)
        self.fill_points(row, points)
        self.fill_additional_points(row, additional_points)
        
    def fill_name(self, row, nickname):
        self.drawtext(self.imdraw,
                      self.markup.name_size["x"], self.markup.dy * row,
                      self.markup.name_size["dx"], self.markup.dy, nickname)
        
    def fill_points(self, row, points):
        self.drawtext(self.imdraw, self.markup.main_points_size["x"], self.markup.dy * row,
                      self.markup.main_points_size["dx"], self.markup.dy, str(points))
        
    def fill_additional_points(self, row, points):
        self.drawtext(self.imdraw, self.markup.additional_points_size["x"], self.markup.dy * row,
                      self.markup.additional_points_size["dx"], self.markup.dy, str(points))        
    
        
        