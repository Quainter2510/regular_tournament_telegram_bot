from PIL import Image, ImageEnhance, ImageDraw, ImageFont
from libs.markup_table import Main_table_markup, Points_tour_markup, Result_tour_markup


class TemplateCreator: 
    def __init__(self, number_of_players, number_of_tour, count_matches_in_tour) -> None:
        self.dark_factor = 0.2
        self.wide_line = 5
        self.thin_line = 1
        self.number_of_players = number_of_players
        self.number_of_tour = number_of_tour
        self.count_matches_in_tour = count_matches_in_tour
    

    def drawtext(self, imdraw, x, y, dx, dy, text, font_size=34):
        font = ImageFont.truetype("images/Fonts/consolas.ttf", size=font_size)
        _, _, w, h = imdraw.textbbox((0, 0), text, font = font)
        text_x = (dx - w) // 2 + x
        text_y = (dy - h) // 2 + y
        imdraw.multiline_text((text_x, text_y), text, font=font, align="center")
        
    def create_all_templates(self, width, height):
        self.create_background(width, height)
        self.create_template_points_tour(width, height)
        self.create_template_result_tour(width, height)
        self.create_template_main_table(width, height)

    def create_background(self, widht, height):
        im = Image.open('images/table_templates/background.jpg')
        im = im.resize((widht, height))

        img = ImageEnhance.Brightness(im).enhance(self.dark_factor)
        img.save("images/table_templates/dark_background.png", "png")

    def create_template_points_tour(self, image_width, image_height):
        markup = Points_tour_markup(self.number_of_players, image_width, image_height)
        img = Image.open("images/table_templates/dark_background.png")
        imdraw = ImageDraw.Draw(img)
        imdraw.line((markup.name_size["x"], 0, markup.name_size["x"],
                     markup.image_height), fill="white", width=self.wide_line)
        imdraw.line((markup.main_points_size["x"], 0, markup.main_points_size["x"], markup.image_height),
                    fill="white", width=self.wide_line)
        imdraw.line((markup.additional_points_size["x"], 0, markup.additional_points_size["x"], markup.image_height),
                    fill="white", width=self.wide_line)
        imdraw.line((0, markup.dy, markup.image_width, markup.dy), fill="white", width=self.wide_line)

        for i in range(1, self.number_of_players + 1):
            imdraw.line((0, markup.dy * i, markup.image_width, markup.dy * i), fill="white", width=self.thin_line)
            self.drawtext(imdraw, markup.place_size["x"], markup.dy * i, markup.place_size["dx"], markup.dy, str(i))

        self.drawtext(imdraw, markup.place_size["x"], 0, markup.place_size["dx"], markup.dy, "Место")
        self.drawtext(imdraw, markup.name_size["x"], 0, markup.name_size["dx"], markup.dy, "Имя")
        self.drawtext(imdraw, markup.main_points_size["x"], 0, markup.main_points_size["dx"], markup.dy, "Очки")
        self.drawtext(imdraw, markup.additional_points_size["x"], 0, markup.additional_points_size["dx"], markup.dy, "Доп Очки")

        img.save("images/table_templates/template_points_tour.png", "png")

    def create_template_result_tour(self, image_width, image_height):
        markup = Result_tour_markup(image_width, image_height, self.count_matches_in_tour)
        img = Image.open("images/table_templates/dark_background.png")
        imdraw = ImageDraw.Draw(img)
        imdraw.line((0, markup.head_size, markup.image_width, markup.head_size),
                    fill="white",
                    width=self.wide_line)    
        imdraw.line((0, image_height - markup.head_size, markup.image_width, image_height - markup.head_size),
                    fill="white",
                    width=self.wide_line) 
        imdraw.line((0, markup.head_size + markup.dy, markup.image_width, markup.head_size + markup.dy),
                    fill="white",
                    width=self.wide_line)  

        for i in range(1, self.count_matches_in_tour + 1):
            imdraw.line((0, markup.head_size + markup.dy * i, markup.image_width, markup.head_size + markup.dy * i),
                        fill="white", width=self.thin_line)  

        imdraw.line((markup.result_size["x"], markup.head_size,
                     markup.result_size["x"], markup.image_height - markup.total_size),
                    fill="white", width=self.wide_line) 
        imdraw.line((markup.forecast_size["x"], markup.head_size, 
                     markup.forecast_size["x"], markup.image_height - markup.total_size),
                    fill="white", width=self.wide_line) 
        imdraw.line((markup.points_size["x"], markup.head_size, markup.points_size["x"], markup.image_height),
                    fill="white", width=self.wide_line) 

        self.drawtext(imdraw, markup.match_size["x"], markup.head_size, markup.match_size["dx"], markup.dy, "Матч")
        self.drawtext(imdraw, markup.result_size["x"], markup.head_size, markup.result_size["dx"], markup.dy, "Результат")
        self.drawtext(imdraw, markup.forecast_size["x"], markup.head_size, markup.forecast_size["dx"], markup.dy, "Прогноз")
        self.drawtext(imdraw, markup.points_size["x"], markup.head_size, markup.points_size["dx"], markup.dy, "Очки")
        self.drawtext(imdraw, markup.match_size["x"], markup.image_height - markup.total_size,
                      markup.points_size["x"], markup.total_size, "Итог за тур")

        # img.show()
        img.save("images/table_templates/template_result_tour.png", "png")

    def create_template_main_table(self, image_width, image_height):      
        markup = Main_table_markup(image_width, image_height, self.number_of_players, self.count_matches_in_tour)

        img = Image.open("images/table_templates/dark_background.png")
        imdraw = ImageDraw.Draw(img)
        imdraw.line((0, markup.head_size, markup.image_width, markup.head_size), fill="white", width=self.wide_line)
        imdraw.line((markup.place_size["x"], 0, markup.place_size["x"], markup.image_height), fill="white", width=self.wide_line)
        imdraw.line((markup.name_size["x"], 0, markup.name_size["x"], markup.image_height), fill="white", width=self.wide_line)
        imdraw.line((markup.tours_size["x"], 0, markup.tours_size["x"], markup.image_height), fill="white", width=self.wide_line)
        imdraw.line((markup.sum_size["x"], 0, markup.sum_size["x"], markup.image_height), fill="white", width=self.wide_line)

        for i in range(1, self.number_of_players + 1):
            imdraw.line((0, markup.head_size + markup.dy * i, markup.image_width,
                         markup.head_size + markup.dy * i), fill="white", width=self.thin_line)
            self.drawtext(imdraw, markup.place_size["x"], markup.head_size + markup.dy * (i - 1),
                     markup.place_size["dx"], markup.dy, str(i))

        tours_dx = markup.tours_size["dx"] / self.number_of_tour

        for i in range(1, self.number_of_tour + 1):
            imdraw.line((markup.tours_size["x"] + tours_dx * i, 0, markup.tours_size["x"] + tours_dx * i, markup.image_height))
            self.drawtext(imdraw, markup.tours_size["x"] + tours_dx * (i - 1), 0, tours_dx, markup.head_size, "Тур\n" + str(i))

        self.drawtext(imdraw, markup.place_size["x"], 0, markup.place_size["dx"], markup.head_size, "№")
        self.drawtext(imdraw, markup.name_size["x"], 0, markup.name_size["dx"], markup.head_size, "Имя")
        self.drawtext(imdraw, markup.sum_size["x"], 0, markup.sum_size["dx"], markup.head_size, "Итог")
        self.drawtext(imdraw, markup.offset_size["x"], 0, markup.offset_size["dx"], markup.head_size, "+/-")

        # img.show()
        img.save("images/table_templates/template_main_table.png", "png")


