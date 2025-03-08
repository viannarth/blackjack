from .player import Player
from .dealer import Dealer
from .deck import Deck
from .wallet import *

from enum import Enum
from datetime import datetime
import json
import os.path

ROUND_HISTORY_FILE = "./usr/round_history.json"
GAME_HISTORY_FILE = "./usr/game_history.json"

class RoundStatus(Enum):
    LOSS = 0
    PUSH = 1
    WIN = 2
    SURRENDER = 3

class Round(object):
    def __init__(self, status:RoundStatus = None, time:datetime = None, profit:float = 0):
        self.status = status
        self.time = time
        self.profit = profit

    def set_status(self, status:RoundStatus):
        self.status = status
    
    def set_time(self, time:datetime):
        self.time = time

    def set_profit(self, profit:float):
        self.profit = profit

    def to_dict(self):
        return {
            "STATUS": self.status.value,
            "TIME": self.time.strftime("%m/%d/%Y %H:%M:%S"),
            "PROFIT": self.profit
        }

class Game(object):
    def __init__(self):
        self.current_round = None
        self.wallet:Wallet = Wallet()
        self.round_history:list[Round] = []
        self.game_history:list[dict] = []
        
    def player_new_card(self, deck:Deck, player:Player):
        return deck.pick_card(player)

    def dealer_new_card(self, deck:Deck, dealer:Dealer):
        return deck.pick_card(dealer)

    def set_player_surrender(self):
        self.current_round.set_status(RoundStatus.SURRENDER)

    def get_wallet(self):
        return self.wallet

    def set_round_profit(self, profit:float):
        self.current_round.set_profit(profit)

    def check_round_history(self):
        if os.path.isfile(ROUND_HISTORY_FILE):
            if os.path.getsize(ROUND_HISTORY_FILE) != 0:
                return True
            return False
        return False

    def get_round_history(self):
        with open(ROUND_HISTORY_FILE, "r") as data_file:
            data = json.load(data_file)
        
        round_history = [
            Round(
                status = RoundStatus(round_data["STATUS"]),
                time = datetime.strptime(round_data["TIME"], "%m/%d/%Y %H:%M:%S"),
                profit = round_data["PROFIT"]
            )
            for round_data in data
        ]
        self.round_history = round_history

        total_profit = sum(round.profit for round in round_history)
        self.wallet.balance = INITIAL_BALANCE + total_profit

    def start_round(self, deck:Deck, player:Player, dealer:Dealer):
        self.current_round = Round()
        deck.create()
        deck.pick_card(player)
        dealer.set_face_up_card(deck)
        deck.pick_card(player)
        deck.pick_card(dealer)

    def check_round_status(self, player:Player, dealer:Dealer):
        if player.bust():
            return RoundStatus.LOSS
        elif dealer.bust():
            return RoundStatus.WIN
        elif player.hand_value > dealer.hand_value:
            return RoundStatus.WIN
        elif player.hand_value < dealer.hand_value:
            return RoundStatus.LOSS
        elif player.blackjack() and not dealer.blackjack():
            return RoundStatus.WIN
        elif not player.blackjack() and dealer.blackjack():
            return RoundStatus.LOSS
        else:
            return RoundStatus.PUSH

    def save_progress(self):
        data = [round.to_dict() for round in self.round_history]

        with open(ROUND_HISTORY_FILE, "w") as data_file:
            json.dump(data, data_file)

    def finish_round(self, player:Player, dealer:Dealer):
        if self.current_round.status != RoundStatus.SURRENDER:
            self.current_round.set_status(self.check_round_status(player, dealer))
        self.current_round.set_time(datetime.now())
        self.round_history.append(self.current_round)
        self.save_progress()
        player.clear_hand()
        dealer.clear_hand()
        
    def game_info(self):
        status_count = {status:0 for status in RoundStatus}

        for round in self.round_history:
            status_count[round.status] += 1
        
        last_played_time = self.round_history[-1].time

        total_profit = sum(round.profit for round in self.round_history)

        return {
            "LOSSES": status_count[RoundStatus.LOSS],
            "PUSHES": status_count[RoundStatus.PUSH],
            "WINS": status_count[RoundStatus.WIN],
            "SURRENDERS": status_count[RoundStatus.SURRENDER],
            "LAST PLAYED TIME": last_played_time.strftime("%m/%d/%Y %H:%M:%S"),
            "TOTAL PROFIT": total_profit
        }
    
    def save_game(self):
        self.game_history.append(self.game_info())

        with open(GAME_HISTORY_FILE, "w") as data_file:
            json.dump(self.game_history, data_file)

    def check_game_history(self):
        if os.path.isfile(GAME_HISTORY_FILE):
            if os.path.getsize(GAME_HISTORY_FILE) != 0:
                return True
            return False
        return False

    def get_game_history(self):
        with open(GAME_HISTORY_FILE, "r") as data_file:
            data = json.load(data_file)
            self.game_history = data

    def clear_round_history(self):
        open(ROUND_HISTORY_FILE, "w").close()
        self.round_history = []

    def clear_game_history(self):
        open(GAME_HISTORY_FILE, "w").close()
        self.game_history = []

    def finish_game(self):
        if len(self.round_history) > 0:
            if self.check_game_history():
                self.get_game_history()
            self.save_game()
            self.current_round = None
            self.wallet.close()
            self.clear_round_history()