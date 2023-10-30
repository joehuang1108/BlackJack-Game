# BlackJack

# Computer -- Dealer
# You -- Player
# Player owns X-amount money
# 100, i bet 100, i win --> 200
#               , i lose --> 0

# 2 cards each
# player can decide to HIT or STAY
# if player HIT:
#   player gets another card
# if player STAY:
#   player stops receiving card and stays at the sum

# After player stays, dealer can HIT or STAY as well
# Both party reveals cards, whoever is closest to 21 without
# going over 21 wins

# Approach:
# 1. Make a deck of cards and mark its values
# 2. Give player two cards along with info
# 3. Prompt player to HIT or STAY
# 4. If HIT, give new card along with info
#       repeat step 3 until STAY
# 5. If STAY, reveal dealers hand
# 6. Compare values and display winner
import random

# Tuple
suits = ('H', 'D', 'S', 'C')
ranking = ('A', '2', '3', '4', '5', '6', '7', '8', '9',
           '10', 'J', 'Q', 'K')
card_val = {'A': 1, '2': 2, '3': 3, '4': 4,
            '5': 5, '6': 6, '7': 7, '8': 8,
            '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10}

chip_pool = 100
print("Your buy-in amount is: $", chip_pool)

# This class helps to make a card (singular)
class Card:
     def __init__(self, suit, rank):
         self.suit = suit
         self.rank = rank
     def __str__(self):
         return self.suit + self.rank
     def grab_suit(self):
         return self.suit
     def grab_rank(self):
         return self.rank
     def draw(self):
         print(self.suit + self.rank)

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0

        # Aces can be a 1 or 11
        self.ace = False

    def __str__(self):
        # Return a string of current hand composition
        hand_comp = ""

        for card in self.cards:
            card_name = card.__str__()
            hand_comp += " " + card_name

        return "The hand has" + hand_comp

    def card_add(self, card):
        # This will add a card to our hand
        self.cards.append(card)

        if card.rank == 'A':
            self.ace = True

        # get the value of this card and add to total value
        value = card_val[card.rank]
        self.value += value
    def calc_val(self):
        # this function will calculate the value of hand (HINT: A = 1 or 11)
        if self.ace == True and self.value < 12:
            return self.value + 10
        else:
            return self.value

    def draw(self, hidden):
        if hidden == True:
            starting_card = 1
        else:
            starting_card = 0
        for x in range(starting_card, len(self.cards)):
            self.cards[x].draw()


class Deck:
    def __init__(self):
        # creating the deck in order
        self.deck = []
        for rank in ranking:
            for suit in suits:
                card = Card(suit, rank)
                self.deck.append(card)
    def shuffle(self):
        # This function will shuffle the deck
        random.shuffle(self.deck)
    def deal(self):
        # This function will spit out one card from the top of deck
        single_card = self.deck.pop()
        return single_card

# End of classes

# BETTING TIME
def make_bet():
    global bet_amount, chip_pool
    bet_amount = input("What amount of chips would you like to bet? ")
    # Ask the player for bet amount

    if bet_amount.isnumeric():
        if int(bet_amount) <= chip_pool:
            print(chip_pool)
            bet_amount = int(bet_amount)
        else:
            print("Invalid amount entered!!! ")
            make_bet()
    else:
        print("Invalid amount entered!!! ")
        make_bet()

def remaining_amount(win):
    global chip_pool, bet_amount
    if win == True:
        chip_pool += bet_amount
    else:
        chip_pool -= bet_amount

# This function will start the dealing process at new game
def deal_cards():
    global deck, player_hand, dealer_hand, playing, bet_amount, chip_pool
    # make an object of Class Deck
    deck = Deck()
    deck.shuffle()
    # Sets up a bet
    make_bet()
    # Set up both the player and dealer hand
    player_hand = Hand()
    dealer_hand = Hand()

    # Deal out initial hand
    player_hand.card_add(deck.deal())
    player_hand.card_add(deck.deal())

    dealer_hand.card_add(deck.deal())
    dealer_hand.card_add(deck.deal())

    # receive input from user for hit or stand
    # result = input("Hit or Stand? Press h for hit, s for stand")

    playing = True
    game_step()


def hit():
    global deck, player_hand, playing, chip_pool, bet_amount
    if player_hand.calc_val() < 21:
        player_hand.card_add(deck.deal())
    else:
        print("Sorry cannot hit")

    if player_hand.calc_val() > 21:
        print("Busted")
        playing = False
        remaining_amount(False)
    game_step()


def stand():
    global deck, player_hand, dealer_hand, playing, chip_pool, bet_amount
    # Dealer hit or stand
    if playing == True:
        while(dealer_hand.calc_val() < 19):
            dealer_hand.card_add(deck.deal())

        print("Dealer Hand is: "), dealer_hand.draw(hidden=False)
        print("Dealer hand total is: " + str(dealer_hand.calc_val()))

        if dealer_hand.calc_val() > 21:
            print("Dealer busted, you win! ")
            remaining_amount(True)
        elif(player_hand.calc_val() > dealer_hand.calc_val()):
            print("You beat the dealer, you win! ")
            remaining_amount(True)
        else:
            print("Dealer wins! ")
            remaining_amount(False)
    playing = False
    player_input()

# runs the game procedure
def game_step():
    global playing
    if playing == False:
        player_input()
    else:
        print("The player's hand is: "), player_hand.draw(hidden=False)
        print("Player hand total is: " + str(player_hand.calc_val()))
        print("")
        print("Dealer Hand is: "), dealer_hand.draw(hidden=True)
        player_input()


def game_exit():
    print("Thanks for playing")
    exit()

# This function will be in charge to processing all players inputs(hit, stand, quit, play again, etc)
def player_input():
    # receives user input
    global playing, chip_pool
    if playing == True:
        plin = input("Would you like to hit, stand, or quit, enter h for hit, s for stand, q for quit: ").lower()
        if plin == 'h':
            hit()
        elif plin == 's':
            stand()
        elif plin == 'q':
            game_exit()
        else:
            print("Invalid Inputs. Enter h or s")
            player_input()
    else:
        print("Your buy-in amount is now: ", chip_pool)
        if chip_pool == 0:
            game_exit()
        plin = input("Would you like play again, or quit, enter p for play again, q for quit: ").lower()
        if plin == 'p':
            deal_cards()
        elif plin == 'q':
            game_exit()
        else:
            print("Invalid Inputs. Enter p or q")
            player_input()

# INTRODUCTION #
def intro():
    print("Welcome to BlackJack! Get as close to 21 as you can without getting over!\n")
    print("Dealer hits until total value reaches 19. Aces count as 1 or 11. "
          "Card output goes by a letter followed by a number of face notations")
    print("Example: H7 = 7 of Hearts\n")

intro()
deal_cards()































