from .player import Player
from .card import *

from random import shuffle

class Deck(object):
    def __init__(self):
        self.cards:list[Card] = []

    def create(self):
        self.cards = [Card(rank, suit) for rank in RANKS for suit in SUITS]
        for card in self.cards:
            if card.rank.isdigit():
                card.value = int(card.rank)
            elif card.rank in ["Jack", "Queen", "King"]:
                card.value = 10
        shuffle(self.cards)
        
    def pick_card(self, player:Player):
        card = self.cards.pop()
        if card.rank == "Ace":
            if player.hand_value < 11:
                card.value = 11
            else:
                card.value = 1
        player.add_card(card)
        
        player.update_ace()
        
        return card