from .card import Card
from .player import Player
from .deck import Deck

class Dealer(Player):
    def __init__(self):
        super().__init__()
        self.face_up:Card = None
    
    def set_face_up_card(self, deck:Deck):
        self.face_up = deck.pick_card(self)
    
    def need_card(self):
        if self.hand_value < 17:
            return True
        return False
    
    def check_soft_17(self):
        if self.hand_value == 17:
            for card in self.hand:
                if card.rank == "Ace" and card.value == 11:
                    return True
            return False
        return False