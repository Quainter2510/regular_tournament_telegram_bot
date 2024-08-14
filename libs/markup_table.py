class Main_table_markup:
    def __init__(self, width, height, number_of_players, count_of_tour):
        self.number_of_players = number_of_players
        self.image_height = height
        self.image_width = width
        self.count_of_tour = count_of_tour
        self.head_size = 80
        self.offset_size = {"x": 0, "dx": 0}
        self.place_size = {"x": 0, "dx": 80}
        self.name_size = {"x": 80, "dx": 540}
        self.tours_size = {"x": 620, "dx": 1180}
        self.sum_size = {"x": 1800, "dx": 120}
        self.dy = (self.image_height - self.head_size) / self.number_of_players
        self.tours_dx = self.tours_size["dx"] / count_of_tour


class Points_tour_markup:
    def __init__(self, number_of_players, width, height):
        self.image_height = height
        self.image_width = width
        self.number_of_players = number_of_players
        self.place_size = {"x": 0, "dx": 150}
        self.name_size = {"x": 150, "dx": 1570}
        self.points_size = {"x": 1720, "dx": 200}
        self.dy = height / (self.number_of_players + 1)


class Result_tour_markup:
    def __init__(self, width, height, count_matches_in_tour):
        self.image_height = height
        self.image_width = width
        self.count_matches_in_tour = count_matches_in_tour
        self.head_size = 150
        self.total_size = 150
        self.dy = (height - self.head_size - self.total_size) / (self.count_matches_in_tour + 1)
        self.match_size = {"x": 0, "dx": 900}
        self.result_size = {"x": 900, "dx": 400}
        self.forecast_size = {"x": 1300, "dx": 400}
        self.points_size = {"x": 1700, "dx": 220}