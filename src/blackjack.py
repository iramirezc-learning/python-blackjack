# Author: Isaac Ramírez, iramirezc@live.com.mx
# Last date modified: 31/10/2015
# Project: Mini-project #6. "Blackjack".
# Course: An Introduction to Interactive Programming in
#         Python (Part 2) @coursera.org

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    
card_back_loc = (CARD_BACK_CENTER[0] + CARD_BACK_SIZE[0] * 0, 
                 CARD_BACK_CENTER[1] + CARD_BACK_SIZE[1] * 0)

# initialize some useful global variables
in_play = False
outcome = ""
color = ""
score = 0

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
# Student should insert code for Hand class here
class Hand:
    def __init__(self):
        # create Hand object
        self.hand_cards = []

    def __str__(self):
        # return a string representation of a hand
        ans = ""
        for i in range(len(self.hand_cards)):
            ans += str(self.hand_cards[i]) + " "
        return "Hand contains " + ans

    def add_card(self, card):
        # add a card object to a hand
        self.hand_cards.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        value = 0
        aces = False
        for i in range(len(self.hand_cards)):
            card_rank = self.hand_cards[i].get_rank()
            card_value = VALUES[card_rank]
            value += card_value
            if card_rank == 'A':
                aces = True
        if aces and (value + 10) <= 21:
            value += 10
                
        return value
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for i in range(len(self.hand_cards)):
            if i <= 5:
                card = self.hand_cards[i]
                card.draw(canvas, pos)
                pos[0] += CARD_SIZE[0]

# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck_cards = []
        for s in SUITS:
            for r in RANKS:
                new_card = Card(s, r)
                self.deck_cards.append(new_card)

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck_cards)

    def deal_card(self):
        # deal a card object from the deck
        card = self.deck_cards.pop()
        return card
    
    def __str__(self):
        # return a string representing the deck
        ans = ""
        for i in range(len(self.deck_cards)):
            ans += str(self.deck_cards[i]) + " "
        return "Deck contains " + ans

#define event handlers for buttons
def deal():
    global in_play, outcome, color, score, deck, player, dealer
    deck = Deck()
    player = Hand()
    dealer = Hand()
    deck.shuffle()
    for i in range(2):
        player.add_card(deck.deal_card())
        dealer.add_card(deck.deal_card())
    if in_play:
        outcome = "OK. But you lost!"
        color = "Red"
        score -= 1
        in_play = False
    else:
        outcome = ""
        in_play = True
    
    # For testing purposes
    print "Player's value: " + str(player.get_value())
    print "Dealer's value: " + str(dealer.get_value())
    print

def hit():
    # if the hand is in play, hit the player
    # if busted, assign a message to outcome, update in_play and score
    global in_play, outcome, color, score, deck, player, dealer
    if in_play:
        if player.get_value() <= 21:
            player.add_card(deck.deal_card())
        if player.get_value() > 21:
            outcome = "You have busted and lost!"
            color = "Red"
            in_play = False
            score -= 1
    # For testing purposes
    print "Player's value: " + str(player.get_value())
    print "Dealer's value: " + str(dealer.get_value())
    print

def stand():
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # assign a message to outcome, update in_play and score
    global in_play, outcome, color, score, deck, player, dealer
    if player.get_value() > 21:
        outcome = "You have busted and lost!"
        color = "Red"
    elif in_play:
        while dealer.get_value() <= 17:
            dealer.add_card(deck.deal_card())
        if dealer.get_value() > 21:
            outcome = "Dealer's busted. You win! Hooray!"
            color = "Lime"
            score += 1
        else:
            if player.get_value() <= dealer.get_value():
                outcome = "Sorry. You lost :("
                color = "Red"
                score -= 1
            else:
                outcome = "Bravo! You win! :)"
                color = "Lime"
                score += 1
        in_play = False
    # For testing purposes
    print "Player's value: " + str(player.get_value())
    print "Dealer's value: " + str(dealer.get_value())
    print

# draw handler    
def draw(canvas):
    global in_play, outcome, color, score, player, dealer
    # Gamename, author and score
    canvas.draw_text("Blackjack", (230, 30), 30, "Black")
    canvas.draw_text("iramirezc@live.com.mx", (235, 45), 12, "Black")
    canvas.draw_text("Score: " + str(score), (450, 100), 30, "White")
    
    # Dealers's hand
    canvas.draw_text("Dealer", (25, 250), 17, "Black")
    canvas.draw_polyline([[105, 200], [95, 200], [95, 296], [105, 296]], 2, 'Black')
    dealer.draw(canvas, [120, 200])
        
    # Player's hand
    canvas.draw_text("Player", (25, 500), 17, "Black")
    canvas.draw_polyline([[105, 450], [95, 450], [95, 546], [105, 546]], 2, 'Black')
    player.draw(canvas, [120, 450])
    
    # Game
    if in_play:
        canvas.draw_image(card_back, card_back_loc, CARD_BACK_SIZE, [120 + CARD_BACK_CENTER[0], 200 + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
        canvas.draw_text("Hit or Stand?", (120, 375), 25, "Yellow")
    else:
        canvas.draw_text(outcome, (120, 150), 25, color)
        canvas.draw_text("New deal?", (120, 375), 25, "Yellow")

# initialization of globals
deck = Deck()
player = Hand()
dealer = Hand()
    
# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()