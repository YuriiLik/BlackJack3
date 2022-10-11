import Player
import random
from constant import MESSAGES
from Deck import Deck



class Game:
    MAX_PL_COUNT = 4

    def __init__(self):
        self.players = []
        self.player = None
        self.player_pos = None
        self.dealer = Player.Dealer()
        self.all_players_count = 1
        self.deck = Deck()
        self.max_bet, self.min_bet = 20, 0


    @staticmethod
    def _ask_starting(message):
        while True:
            choice = input(message)
            if choice == 'n':
                return False
            elif choice == 'y':
                return True

    def _launching(self):
        bots_count = 0
        while True:
            bots_count = int(input('Введіть кількість додаткових гравців (не більше трьох):'))
            if bots_count <= self.MAX_PL_COUNT-1:
                break
        self.all_players_count = bots_count + 1

        for _ in range(bots_count):
            b = Player.Bot()
            self.players.append(b)
            print('Гравець', b, 'долучився до гри')

        self.player = Player.Player()
        self.player_pos = random.randint(0, self.all_players_count)
        print('Ви граєте під номером', self.player_pos)
        self.players.insert(self.player_pos, self.player)

    def ask_bet(self):
        for player in self.players:
            player.change_bet(self.max_bet, self.min_bet)

    def first_descr(self):
        for player in self.players:
            for _ in range(2):
                card = self.deck.get_card()
                player.take_card(card)

        card = self.deck.get_card()
        self.dealer.take_card(card)
        self.dealer.print_cards()

    def check_stop(self, player):
        if player.full_points >= 21:
            return True
        else:
            return False

    def remove_player(self, player):
        player.print_cards()
        if isinstance(player, Player.Player):
            print('Друже, у тебе перебір')
        elif isinstance(player, Player.Bot):
            print('У гравця', player, 'перебір!')
        self.players.remove(player)

    def ask_cards(self):
        for player in self.players:
            while player.ask_card():
                card = self.deck.get_card()
                player.take_card(card)
                is_stop = self.check_stop(player)
                if is_stop:
                    if player.full_points > 21 or isinstance(player, Player.Player):
                        self.remove_player(player)
                    break

                if isinstance(player, Player.Player):
                    player.print_cards()

    def check_winner(self):
        if self.dealer.full_points > 21:
            # all win
            print('У Дилера перебір! Усі гравці виграли!')
            for winner in self.players:
                winner.money += winner.bet * 2

        else:
            for player in self.players:
                if player.full_points == self.dealer.full_points:
                    player.money += player.bet
                    print(MESSAGES.get('eq').format(player=player,
                                                    points=player.full_points))
                elif player.full_points > self.dealer.full_points:
                    player.money += player.bet * 2
                    if isinstance(player, Player.Bot):
                        print(MESSAGES.get('win').format(player))
                    elif isinstance(player, Player.Player):
                        print('Молодець, ти виграв!')

                elif player.full_points < self.dealer.full_points:
                    if isinstance(player, Player.Bot):
                        print(MESSAGES.get('lose').format(player))
                    elif isinstance(player, Player.Player):
                        print('На жаль тобі не пощастило, ти програв!')

    def play_with_dealer(self):
        while self.dealer.ask_card():
            card = self.deck.get_card()
            self.dealer.take_card(card)
        self.dealer.print_cards()

    def start_game(self):
        message = MESSAGES.get('ask_start')

        if not self._ask_starting(message=message):
            exit(1)

        # generating data for starting
        self._launching()

        while True:
            # ask about bet
            self.ask_bet()

            # give first cards to the players
            self.first_descr()

            # print player cards after first deal
            self.player.print_cards()

            # ask players about cards
            self.ask_cards()

            self.play_with_dealer()

            self.check_winner()

            print('Гра завершена, заходьте до нашого клубу ще!\nНе забудь задонатити на ЗСУ!')


            break
