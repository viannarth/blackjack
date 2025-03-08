from .deck import Deck
from .player import Player
from .dealer import Dealer
from .game import RoundStatus, Game
from .wallet import *

import os

class ScreenManager(object):
    def __init__(self):
        self.current_screen = None
        self.screens = {}
        self.running = True

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def get_screen(self, screen):
        if screen not in self.screens:
            self.screens[screen] = screen(self)
        return self.screens[screen]
    
    def navigate_to(self, screen):
        self.current_screen = self.get_screen(screen)

    def run(self, deck:Deck, player:Player, dealer:Dealer, game:Game):
        self.clear_screen()

        self.navigate_to(MainMenu)

        while self.running:
            self.current_screen.display(self, deck, player, dealer, game)
        
    def stop(self):
        self.clear_screen()

        self.running = False


class Screen(object):
    def __init__(self, manager:ScreenManager):
        self.manager = manager
    
    def display(self, manager:ScreenManager, deck:Deck, player:Player, dealer:Dealer, game:Game):
        raise NotImplementedError


class MainMenu(Screen):
    def __init__(self, manager):
        super().__init__(manager)
    
    def display(self, manager, deck, player, dealer, game):
        manager.clear_screen()

        print("======== GAGO'S BLACKJACK ========")
        print("\n1 - CONTINUE")
        print("2 - START NEW GAME")
        print("3 - GAME HISTORY")
        print("4 - GAME STATISTICS")
        print("5 - EXIT\n")

        user_input = None
        while user_input not in ["1", "2", "3", "4", "5"]:
            user_input = input("Select an option: ")
            if user_input == "1":
                manager.navigate_to(ContinueGame)
            elif user_input == "2":
                manager.navigate_to(NewGame)
            elif user_input == "3":
                manager.navigate_to(GameHistory)
            elif user_input == "4":
                manager.navigate_to(GameStatistics)
            elif user_input == "5":
                manager.stop()


class GameStatistics(Screen):
    def __init__(self, manager):
        super().__init__(manager)

    def display(self, manager, deck, player, dealer, game):
        manager.clear_screen()

        print("======== GAGO'S BLACKJACK ========\n")
        print("STATISTICS OF ALL THE PREVIOUS GAMES IN THE CURRENT SAVE:\n")
        
        if game.check_game_history():
            game.get_game_history()

            num_games = len(game.game_history)

            print(f"NUMBER OF GAMES: {num_games}")

            game_status = ["LOSSES", "PUSHES", "WINS", "SURRENDERS"]
            status_count = {status:0 for status in game_status}

            for game_ in game.game_history:
                for key in game_:
                    if key in game_status:
                        status_count[key] += game_[key]

            total_profit:float = sum(game_["TOTAL PROFIT"] for game_ in game.game_history)

            for status, value in status_count.items():
                print(f"{status}: {value}")
            
            print(f"TOTAL PROFIT: {total_profit:.2f}$")

            num_rounds = sum(status_count.values())
            mean_profit:float = total_profit / num_rounds

            print(f"AVERAGE PROFIT PER ROUND: {mean_profit:.2f}$")

            win_rate:float = status_count["WINS"] / num_rounds

            print(f"WIN RATE: {(100 * win_rate):.2f}%")
        else:
            print("\nThis save has no previous games. Play and save games to view its statistics.")
        
        input("\nPress Enter to return. ")
        manager.navigate_to(MainMenu)


class ContinueGame(Screen):
    def __init__(self, manager):
        super().__init__(manager)
    
    def display(self, manager, deck, player, dealer, game):
        if game.check_round_history():
            game.get_round_history()
            manager.navigate_to(RoundMenu)

        else:
            manager.clear_screen()

            print("======== GAGO'S BLACKJACK ========")
            print("\nYou need to start a new game before continue. Dur.")
            input("\nPress Enter to return. ")
            manager.navigate_to(MainMenu)


class NewGame(Screen):
    def __init__(self, manager):
        super().__init__(manager)

    def display(self, manager, deck, player, dealer, game):
        if game.check_round_history():
            game.get_round_history()

            manager.clear_screen()

            print("======== GAGO'S BLACKJACK ========")
            print("\nYou will lose all current game data and you will start a game from the scratch. Are you sure you want to proceed?")
            print("\n1 - YES")
            print("2 - NO\n")

            user_input = None
            while user_input not in ["1", "2"]:
                user_input = input("Select an option: ")
                if user_input == "1":
                    game.finish_game()
                    input("\nYour game has been deleted. Press Enter to start a new game. ")
                    manager.navigate_to(RoundMenu)
                elif user_input == "2":
                    manager.navigate_to(MainMenu)
        else:
            manager.navigate_to(RoundMenu)


class GameHistory(Screen):
    def __init__(self, manager):
        super().__init__(manager)

    def clear_game_history(self, manager:ScreenManager, game:Game):
        print("\nYou are about to clear all the previous game history, including it statistics. Are you sure you want to proceed?")
        print("\n1 - YES")
        print("2 - NO\n")

        user_input2 = None
        while user_input2 not in ["1", "2"]:
            user_input2 = input("Select an option:" )
            if user_input2 == "1":
                game.clear_game_history()
                manager.navigate_to(GameHistory)
            elif user_input2 == "2":
                manager.navigate_to(GameHistory)        

    def display(self, manager, deck, player, dealer, game):
        manager.clear_screen()
        print("======== GAGO'S BLACKJACK ========")
        print("\nPREVIOUS GAMES")

        if game.check_game_history():
            game.get_game_history()

            for idx, game_ in enumerate(game.game_history):
                print(f"\nGAME {idx+1}:")
                for key, value in game_.items():
                    if key == "TOTAL PROFIT":
                        value = str(value) + "$"
                    print(f"\t{key}: {value}")
        else:
            print("\nThis save has no previous games.")

        print("\nCURRENT GAME:\n")

        if game.check_round_history():
            game.get_round_history()
            dict_info = game.game_info()
            for key, value in dict_info.items():
                if key == "TOTAL PROFIT":
                    value = str(value) + "$"
                print(f"\t{key}: {value}")   
        else:
            print("This game has no rounds yet.")

        print("\n1 - RETURN TO MAIN MENU")
        print("2 - CLEAR PREVIOUS GAME HISTORY\n")

        user_input = None
        while user_input not in ["1", "2"]:
            user_input = input("Select an option: ")
            if user_input == "1":
                manager.navigate_to(MainMenu)
            elif user_input == "2":
                if(game.check_game_history()):
                    self.clear_game_history(manager, game)
                else:
                    print("\nYou need to have previous game history before clean it. Hur dur. Don't get smart with me.")
                    input("\nPress Enter to return. ")
                    manager.navigate_to(GameHistory)


class RoundMenu(Screen):
    def __init__(self, manager):
        super().__init__(manager)

    def display(self, manager, deck, player, dealer, game):
        manager.clear_screen()

        print("======== GAGO'S BLACKJACK ========")
        print("\n1 - START NEW ROUND")
        print("2 - ROUND HISTORY")
        print("3 - ROUND STATISTICS")
        print("4 - RETURN TO MAIN MENU\n")

        print(f"YOUR BALANCE: {game.get_wallet().balance:.2f}$\n")

        user_input = None
        while user_input not in ["1", "2", "3", "4"]:
            user_input = input("Select an option: ")
            if user_input == "1":
                manager.navigate_to(InRound)
            elif user_input == "2":
                manager.navigate_to(RoundHistory)
            elif user_input == "3":
                manager.navigate_to(RoundStatistics)
            elif user_input == "4":
                manager.navigate_to(MainMenu)


class RoundHistory(Screen):
    def __init__(self, manager):
        super().__init__(manager)
    
    def display(self, manager, deck, player, dealer, game):
        manager.clear_screen()

        print("======== GAGO'S BLACKJACK ========")
        print("\nROUND HISTORY OF THE CURRENT GAME")

        if game.check_round_history():
            game.get_round_history()
            for idx, round in enumerate(game.round_history):
                print(f"\nROUND {idx+1}:")
                dict_round = round.to_dict()
                for key, value in dict_round.items():
                    if key == "STATUS":
                        value = RoundStatus(value).name
                    if key == "PROFIT":
                        value = str(value) + "$"
                    print(f"\t{key}: {value}")
        else:
            print("\nThis game has no rounds yet.")

        input("\nPress Enter to return. ")
        manager.navigate_to(RoundMenu)


class RoundStatistics(Screen):
    def __init__(self, manager):
        super().__init__(manager)

    def display(self, manager, deck, player, dealer, game):
        manager.clear_screen()

        print("======== GAGO'S BLACKJACK ========")
        print("\nROUND STATISTICS OF THE CURRENT GAME")

        if game.check_round_history():
            game.get_round_history()

            num_rounds = len(game.round_history)
            print(f"\nNUMBER OF ROUNDS: {num_rounds}")

            status_count = {status:0 for status in RoundStatus}
            for round in game.round_history:
                status_count[round.status] += 1

            for status, value in status_count.items():
                print(f"{RoundStatus(status).name}: {value}")

            win_rate:float = status_count[RoundStatus.WIN] / sum(status_count.values())
            print(f"WIN RATE: {(100 * win_rate):.2f}%")

            total_profit = sum(round.profit for round in game.round_history)
            print(f"TOTAL PROFIT: {total_profit:.2f}$")
            mean_profit:float = total_profit / num_rounds
            print(f"AVERAGE PROFIT PER ROUND: {mean_profit:.2f}$")
        else:
            print("\nThis game has no rounds yet. Play rounds to view its statistics.")

        input("\nPress Enter to return. ")
        manager.navigate_to(RoundMenu)


class InRound(Screen):
    def __init__(self, manager):
        super().__init__(manager)
    
    def set_bet(self, game:Game):
        print("======== GAGO'S BLACKJACK ========")
        print("\nCHOOSE YOUR BET:\n")
        for key, value in INITIAL_BET.items():
            print(f"{key} - {value}$")
        print(f"{len(INITIAL_BET)+1} - RETURN\n")

        valid_options = [key for key in INITIAL_BET] + [f"{len(INITIAL_BET)+1}"]
        user_input = None
        while user_input not in valid_options:
            user_input = input("Select an option: ")
            for key in INITIAL_BET:
                if user_input == key:
                    game.get_wallet().set_initial_bet(user_input)
                    
                    print(f"\nYou lost, I mean, you bet {INITIAL_BET[user_input]}$.")
                    input("\nPress Enter to continue. ")
                    return True
                elif user_input == f"{len(INITIAL_BET)+1}":
                    return False

    def insurance_bet(self, game:Game):
        print("\nPress Enter to continue. ")

        print(f"\nSince the card is an Ace, you can bet if the dealer has a blackjack. Do you want to bet {INSURANCE_BET}$?")
        print("1 - YES")
        print("2 - NO\n")

        user_input = None
        while user_input not in ["1", "2"]:
            user_input = input("Select an option: ")
            if user_input == "1":
                game.get_wallet().choose_insurance_bet = True
            elif user_input == "2":
                game.get_wallet().choose_insurance_bet = False

    def first_question(self, manager:ScreenManager, deck:Deck, player:Player, dealer:Dealer, game:Game):
            print("\nThe dealer asks you whether you want another card of the deck.")
            print("\n1 - HIT")
            print("2 - STAND")
            print("3 - DOUBLE DOWN")
            print("4 - SURRENDER\n")

            user_input = None
            while user_input not in ["1", "2", "3", "4"]:
                user_input = input("Select an option: ")
                if user_input == "1":
                    self.player_hit(manager, deck, player, dealer, game)
                elif user_input == "2":
                    self.player_stand(manager, deck, player, dealer, game)
                elif user_input == "3":
                    self.double_down(manager, deck, player, dealer, game)
                elif user_input == "4":
                    self.player_surrender(manager, player, dealer, game)

    def no_double_question(self, manager:ScreenManager, deck:Deck, player:Player, dealer:Dealer, game:Game):
            print("\nThe dealer asks you whether you want another card of the deck.")
            print("\n1 - HIT")
            print("2 - STAND")
            print("3 - SURRENDER\n")

            user_input = None
            while user_input not in ["1", "2", "3"]:
                user_input = input("Select an option: ")
                if user_input == "1":
                    self.player_hit(manager, deck, player, dealer, game)
                elif user_input == "2":
                    self.player_stand(manager, deck, player, dealer, game)
                elif user_input == "3":
                    self.player_surrender(manager, player, dealer, game)
    
    def player_hit(self, manager:ScreenManager, deck:Deck, player:Player, dealer:Dealer, game:Game):
        new_card = game.player_new_card(deck, player)
        print("\nThe dealer deals a card to you. This card is:")
        new_card.print()
        print("\nSo your new hand is:")
        player.print_cards()
        print(f"\nYour hand now has a value of {player.hand_value}.")

        input("\nPress Enter to continue. ")

        if player.bust():
            self.player_bust(manager, player, dealer, game)
        else:
            self.no_double_question(manager, deck, player, dealer, game)

    def player_stand(self, manager:ScreenManager, deck:Deck, player:Player, dealer:Dealer, game:Game):
        print("\nYou chose stand with your hand. Let's see if it was a good choice...")

        self.dealer_reveal_card(dealer, game)
        self.dealer_action(deck, dealer, game)
        self.round_result(player, dealer,game)
        self.finish_round(manager, player, dealer, game)

    def double_down(self, manager:ScreenManager, deck:Deck, player:Player, dealer:Dealer, game:Game):
        print("\nSo you think you are all that and a bag of chips... Double-down the bet!")
        game.get_wallet().double()
        new_card = game.player_new_card(deck, player)
        print("\nThe dealer deals a card to you. This card is:")
        new_card.print()
        print("\nSo your new hand is:")
        player.print_cards()
        print(f"\nYour hand now has a value of {player.hand_value}.")

        input("\nPress Enter to continue. ")

        if player.bust():
            self.player_bust(manager, player, dealer, game)
        else:
            self.dealer_reveal_card(dealer, game)
            self.dealer_action(deck, dealer, game)
            self.round_result(player, dealer, game)
            self.finish_round(manager, player, dealer, game)

    def player_surrender(self, manager:ScreenManager, player:Player, dealer:Dealer, game:Game):
        game.get_wallet().surrender(game)
        print("\nSo you chose the safest way... I don't wanna judge. Weak.")
        print(f"\nYou lose {-game.get_wallet().profit}$.")

        game.set_player_surrender()
        self.finish_round(manager, player, dealer, game)

    def player_bust(self, manager:ScreenManager, player:Player, dealer:Dealer, game:Game):
        game.get_wallet().loss(game)
        print("\nYou bust! What an idiot... Be more careful next time.")
        print(f"\nYou lose {-game.get_wallet().profit}$.")

        self.finish_round(manager, player, dealer, game)

    def dealer_soft_17(self, deck:Deck, dealer:Dealer, game:Game):
        print("\nOh, that's a soft 17! For your luck (or bad luck?), the dealer has to hit a card.")
        new_card = game.dealer_new_card(deck, dealer)
        print("\nThe dealer's new card is:")
        new_card.print()
        print("\nAfter all, the dealer has the following hand:")
        dealer.print_cards()
        print(f"\nFinally, the dealer's hand now values {dealer.hand_value}.")

        input("\nPress Enter to continue. ")

    def dealer_action(self, deck:Deck, dealer:Dealer, game:Game):        
        if dealer.check_soft_17():
                self.dealer_soft_17(deck, dealer, game)
                
        while dealer.need_card():
            print("\nThe dealer has to deal another card for himself.")
            new_card = game.dealer_new_card(deck, dealer)
            print("\nThe dealt card is:")
            new_card.print()
            print("\nThus, the dealer's new hand is:")
            dealer.print_cards()
            print(f"\nThe dealer's hand now values {dealer.hand_value}.")

            input("\nPress Enter to continue. ")

            if dealer.check_soft_17():
                self.dealer_soft_17(deck, dealer, game)

        if dealer.bust():
            print("\nOh, the dealer busts! How luck of you.")                      
            
    def dealer_reveal_card(self, dealer:Dealer, game:Game):
        print("\nThe dealer reveals the face-down card and his hand is:")
        dealer.print_cards()
        print(f"\nTherefore, his hand has a value of {dealer.hand_value}.")

        if dealer.blackjack():
            print("\nThe dealer got a blackjack!")
            if game.get_wallet().choose_insurance_bet:
                game.get_wallet().insurance_bet(True)
                print(f"\nCongrats! You win your insurance bet. You received {INSURANCE_BET}$.")
            
        if game.get_wallet().choose_insurance_bet:
            game.get_wallet().insurance_bet(False)
            print(f"\nThe dealer does not have a blackjack, so you lost your bet. Less {INSURANCE_BET}$ in your account. Fool.")

        input("\nPress Enter to continue. ")

    def round_result(self, player:Player, dealer:Dealer, game:Game):
        if game.check_round_status(player, dealer) == RoundStatus.LOSS:
            game.get_wallet().loss(game)
            print("\nYou lost. Moron.")
            print(f"\nYou lose {-game.get_wallet().profit}$.")
        elif game.check_round_status(player, dealer) == RoundStatus.PUSH:
            game.get_wallet().push(game)
            print("\nIt is a push! That was close.")
            print(f"\nYou get your {game.get_wallet().initial_bet}$ bet back.")
        elif game.check_round_status(player, dealer) == RoundStatus.WIN:
            game.get_wallet().win(game)
            print("\nCongrats! You win. You are lucky.")
            print(f"\nYou win {game.get_wallet().profit}$.")

    def finish_round(self, manager:ScreenManager, player:Player, dealer:Dealer, game:Game):
        game.finish_round(player, dealer)

        print("\nRound finished.")

        print("\n1 - START NEW ROUND")
        print("2 - RETURN\n")

        user_input = None
        while user_input not in ["1", "2"]:
            user_input = input("Select an option: ")
            if user_input == "1":
                manager.navigate_to(InRound)
            elif user_input == "2":
                manager.navigate_to(RoundMenu)
    
    def display(self, manager, deck, player, dealer, game):
        if(self.set_bet(game)):   
            manager.clear_screen()

            game.start_round(deck, player, dealer)

            print("======== GAGO'S BLACKJACK ========")
            print("\nThe dealer deals two cards face-up to you and one card face-up to him. Furthermore, he deals one card face-down to himself.")
            print("\nThe cards in your hand is:")
            player.print_cards()
            print(f"\nThus, you have a hand with a value of {player.hand_value}.")

            print("\nThe dealer's face-up card is a:")
            dealer.face_up.print()
            print(f"\nThis card has a value of {dealer.face_up.value}.")

            if dealer.face_up.rank == "Ace":
                self.insurance_bet(game)

            input("\nPress Enter to continue. ")

            if player.blackjack():
                print("\nCongratulations! You got a blackjack!")
                self.dealer_reveal_card(dealer, game)
                self.round_result(player, dealer, game)
                self.finish_round(manager, player, dealer, game)
            else:
                self.first_question(manager, deck, player, dealer, game)
        else:
            manager.navigate_to(RoundMenu)