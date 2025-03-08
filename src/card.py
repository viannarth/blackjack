RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
SUITS = ["Clubs", "Hearts", "Spades", "Diamonds"]

class Card(object):
    def __init__(self, rank:str, suit:str, value:int = 0):
        self.rank = rank
        self.suit = suit
        self.value = value
    
    def print(self):
        print(self.rank, "of", self.suit)