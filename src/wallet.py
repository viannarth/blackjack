INITIAL_BALANCE = 1000
CHIPS = [10, 25, 50, 100, 250, 500, 1000, 2500]
INITIAL_BET = {str(idx+1):val for idx, val in enumerate(CHIPS)}
INSURANCE_BET = 100

class Wallet(object):
    def __init__(self):
        self.balance:float = INITIAL_BALANCE
        self.initial_bet:float = 0
        self.profit:float = 0
        self.choose_insurance_bet:bool = False
    
    def new_bet(self):
        self.choose_insurance_bet = False
        self.profit = 0
    
    def set_initial_bet(self, input:str):
        self.new_bet()
        self.initial_bet = INITIAL_BET[input]
    
    def finish_bet(self, profit:float, game):
        self.profit += profit
        self.balance += self.profit
        game.set_round_profit(self.profit)
    
    def win(self, game):
        profit:float = self.initial_bet
        self.finish_bet(profit, game)
    
    def loss(self, game):
        profit:float = -self.initial_bet
        self.finish_bet(profit, game)

    def push(self, game):
        profit:float = 0 * self.initial_bet
        self.finish_bet(profit, game)
    
    def surrender(self, game):
        profit:float = -0.5 * self.initial_bet
        self.finish_bet(profit, game)

    def insurance_bet(self, check_win:bool):
        if check_win:
            self.profit += INSURANCE_BET
        else:
            self.profit -= INSURANCE_BET
    
    def double(self):
        self.initial_bet *= 2
    
    def close(self):
        self.balance = INITIAL_BALANCE
        self.initial_bet = 0