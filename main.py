from src.player import Player
from src.deck import Deck
from src.dealer import Dealer
from src.game import Game
from src.screens import ScreenManager

def main():
    deck = Deck()
    player = Player()
    dealer = Dealer()
    game = Game()
    manager = ScreenManager()

    manager.run(deck, player, dealer, game)

if __name__ == "__main__":
    main()