from libs.markup_table import Main_table_markup, Points_tour_markup, Result_tour_markup
from PIL import ImageDraw, ImageFont, Image
from config import config
from database.common import Base

class ImageFiller:
    def __init__(self, database: Base, width, height, filename) -> None:
        self.database: Base = database
        self.width = width
        self.height = height
        self.filename = filename
        
        
    def drawtext(self, imdraw: ImageDraw.ImageDraw, x, y, dx, dy, text, color_fill="white"):
        font = ImageFont.truetype("images/Fonts/consolas.ttf", size=42)
        _, _, w, h = imdraw.textbbox((0, 0), text, font = font)
        text_x = (dx - w) // 2 + x
        text_y = (dy - h) // 2 + y
        imdraw.multiline_text((text_x, text_y), text, font=font, align="center", fill=color_fill)
        
    def create_imagedraw(self):
        self.img = Image.open(f"images/table_templates/template_{self.filename}.png")
        self.imdraw = ImageDraw.Draw(self.img)
        
    def save_image(self):
        self.img.save(f"images/ready_tables/{self.filename}.png")
        
    
    
        
        