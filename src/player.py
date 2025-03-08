from .card import Card

class Player(object):
    def __init__(self):
        self.hand:list[Card] = []
        self.hand_value:int = 0

    def add_card(self, card:Card):
        self.hand.append(card)
        self.hand_value += card.value
    
    def update_ace(self):
        if self.hand_value > 21:
            for card in self.hand:
                if card.rank == "Ace" and card.value == 11:
                    card.value = 1
                    self.hand_value -= 10

    def clear_hand(self):
        self.hand = []
        self.hand_value = 0
    
    def print_cards(self):
        for card in self.hand:
            card.print()

    def blackjack(self):
        if len(self.hand) == 2 and self.hand_value == 21:
            return True
        return False
    
    def bust(self):
        if self.hand_value > 21:
            return True
        return False