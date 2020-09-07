# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
hitMsg = ""

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        handString = "Hand contains"	# return a string representation of a hand
        i = 0

        while (i < len(self.cards)):
            handString = handString + " " + self.cards[i].suit + self.cards[i].rank
            i += 1

        return handString

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        aces = 0
        valueSum = 0
        i = 0

        while(i < len(self.cards)):

            if (aces > 1) and (valueSum + 10 <= 21):
                valueSum = valueSum + 10

            valueSum = valueSum + VALUES[self.cards[i].rank]

            if self.cards[i].rank == "A":
                aces += 1

            i +=1

        return valueSum

    def draw(self, canvas, pos):
    # draw a hand on the canvas, use the draw method for cards
        i=0
        while(i < len(self.cards)):
            self.cards[i].draw(canvas, [pos[0] + CARD_CENTER[0] + i * (30 + CARD_SIZE[0]), pos[1] + CARD_CENTER[1]])
            i=i+1


# define deck class
class Deck:
    def __init__(self):
    # create a Deck object

        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit,rank))

        return self.deck


    def shuffle(self):
        # shuffle the deck
        return random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()

    def __str__(self):
        # return a string representing the deck
        deckString = "Deck contains"
        i = 0
        while (i < len(self.deck)):
            deckString = deckString + " " + self.deck[i].suit + self.deck[i].rank
            i += 1
        return deckString



#define event handlers for buttons
def deal():
    global outcome, in_play, deckDeal, score, player, dealer, hitMsg

    deckDeal = Deck()
    deckDeal.shuffle()
    outcome = ''
    hitMsg = ''

    if in_play == True:
        score -= 1
    else:
        in_play = True

    player = Hand()

    player.add_card(deckDeal.deal_card())
    player.add_card(deckDeal.deal_card())
    outcome = "Hit or Stand"
    print player

    dealer = Hand()

    dealer.add_card(deckDeal.deal_card())
    dealer.add_card(deckDeal.deal_card())

    print dealer



def hit():
    global deckDeal, score, player, dealer, in_play, hitMsg, outcome

    if in_play:
        player.add_card(deckDeal.deal_card())
        if player.get_value() > 21:
            in_play = False
            score -= 1
            hitMsg = "Busted! Dealer wins"
            outcome = "Click deal to play again"

        elif player.get_value() == 21 and dealer.get_value() == 21:
            in_play = False
            score -= 1
            hitMsg = "Dealer wins"
            outcome = "Click deal to play again"

        elif player.get_value() == 21:
            in_play = False
            score += 1
            hitMsg = "You Win!"
            outcome = "Click deal to play again"

    # if the hand is in play, hit the player

    # if busted, assign a message to outcome, update in_play and score

def stand():
    global deckDeal, score, player, dealer, in_play, hitMsg, outcome

    if in_play:
        while dealer.get_value() < 17:
            dealer.add_card(deckDeal.deal_card())

        if dealer.get_value() >= player.get_value() and dealer.get_value() <= 21:
            hitMsg = "Dealer wins!"
            outcome = "Click deal to play again"
            score -= 1
            in_play = False

        elif dealer.get_value() >= player.get_value():
            hitMsg = "Player wins!"
            outcome = "Click deal to play again"
            score += 1
            in_play = False

    print dealer, player

    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score

# draw handler
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global in_play, dealer, player, hitMsg, outcome
    canvas.draw_text("Blackjack", [50, 50], 40, "White")
    canvas.draw_text("Score: " + str(score), [700, 150], 20, "White")
    canvas.draw_text("Player", [80, 375], 25, "White")
    canvas.draw_text("Dealer", [80, 150], 25, "White")
    canvas.draw_text(hitMsg, [500, 50], 25, "White")
    canvas.draw_text(outcome, [500, 100], 25, "white")
    dealer.draw(canvas, [100, 180])

    player.draw(canvas, [100, 400])


# initialization frame
frame = simplegui.create_frame("Blackjack", 800, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
