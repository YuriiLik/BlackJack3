import abc
import random
from Deck import Deck
from constant import MESSAGES


class AbstractPlayer(abc.ABC):
    def __init__(self):
        self.cards = []
        self.bet = 0
        self.full_points = 0
        self.money = 100

    def change_points(self):
        self.full_points = sum([card.points for card in self.cards])

    def take_card(self, card):
        self.cards.append(card)
        self.change_points()

    @abc.abstractmethod
    def change_bet(self, max_bet, min_bet):
        pass

    def print_cards(self):
        print(self, "'інформація про гравця'")
        for card in self.cards:
            print(card)
        print('Усього очків:', self.full_points)

    @abc.abstractmethod
    def ask_card(self, deck):
        pass


class Player(AbstractPlayer):

    def change_bet(self, max_bet, min_bet):
        while True:
            value = int(input('Зробіть Вашу ставку:'))
            if value < max_bet and value > min_bet:
                self.bet = value
                break
        print('Ваша ставка становить:', self.bet)

    def ask_card(self):
        choice = input(MESSAGES.get('ask_card'))
        if choice == 'y':
            return True
        else:
            return False


class Dealer(AbstractPlayer):

    max_points = 17

    def change_bet(self, max_bet, min_bet):
        """
        NOTE: This type is Dealer so it has no bets
        """""
        raise Exception('This type is dealer so it has no bets')

    def ask_card(self):
        if self.full_points < self.max_points:
            return True
        else:
            return False


class Bot(AbstractPlayer):

    def __init__(self):
        super().__init__()
        self.max_points = random.randint(17, 20)

    def change_bet(self, max_bet, min_bet):
        self.bet = random.randint(min_bet, max_bet)
        print('Гравець:', self, 'зробив наступну ставку:', self.bet)

    def ask_card(self):
        if self.full_points < self.max_points:
            return True
        else:
            return False
