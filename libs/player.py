from config.config import config
from libs.tournament_error import TournamentError

class Player:
    def __init__(self, nickname, tg_id) -> None:
        self.possible_statuses_for_users = ("admin", "player")
        self.possible_payments_for_users = ("debtor", "paid")
        self.nickname = nickname
        self.id = tg_id
        self.payment = "debtor"
        if self.id == config.ADMIN_ID:
            self.status = "superadmin"
        else:
            self.status = "player"

    def set_nickname(self, new_nickname) -> None:
        self.nickname = new_nickname
        
    def set_status(self, status):
        if status in self.possible_statuses_for_users:
            raise TournamentError("unknown status")
        self.status = status
        
