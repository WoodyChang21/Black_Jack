from tkinter import E

#Global Enrionment
#The random library is imported for Deck class
from asyncio.windows_events import NULL
import random

#Suits and ranks are listed in the tuple cause we don't want to accidentally modify it
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 
            'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}
count_values = {'Two':1, 'Three':1, 'Four':1, 'Five':1, 'Six':1, 'Seven':0, 'Eight':0, 
            'Nine':0, 'Ten':-1, 'Jack':-1, 'Queen':-1, 'King':-1, 'Ace':-1}

def intro():
    print("Welcome to BlackJack! Get as close to 21 as you can without going over!")
    print("Player can choose to hit, stand, or double down ")
    print("Dealer hits until she reaches 17. Aces count as 1 or 11.")


#Card Class
#Suit, Rank, Value
class Card():
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        #It returns the integer value of the rank
        self.value = values[rank]
        #It returns the digital value to print out on the terminal
        self.count = count_values[rank]
        
    def __str__(self):
        return (self.rank + " of " + self.suit)

class Deck():
    
    def __init__(self):
        self.all_cards = []

    def create_new_deck(self):   
        for suit in suits:
            for rank in ranks:
                #Create the card object by calling the Card Class which provides unique suit and rank
                created_card = Card(suit, rank)
                self.all_cards.append(created_card)
        #This function doesn't return anything but shuffle the deck
    def shuffle(self):
        #Since we only have "import random" --> random.shuffle(list)
        #If we have "From random import shuffle" --> shuffle(list)
        #It doesn't return anything, it only affect the list itsel
        #the self.all_cards is already shuffled
        random.shuffle(self.all_cards)
    
    def deal_one(self):
        #the self.all_cards is a list
        return self.all_cards.pop()
    
    def check_deck(self):
        global count
        if len(self.all_cards)<10:
            self.all_cards = []
            self.create_new_deck()
            self.shuffle()
            print("This deck is almost out of card! The deck has been updated and shuffled! Running Count now is equal to 0")
            count = 0

        else:
            print("This deck has enough card to play")


class Player():
    def __init__(self,name,balance):
        self.balance = balance
        self.name = name

    #Player places the bet
    def bet(self,money):

        if type(money)!=int:
            print("Please enter valid amount of money")
        elif money>self.balance:
            print(f"{self.name} has insufficient balance! Current balance: {self.balance}")
            return NULL
        else:
            print("Bet has successfully placed")
        
        return money
    #Player add money (Win bet, add balance)
    def add_money(self,money):

        if type(money)!=int:
            print("Please enter valid amount of money")
        else:
            self.balance = self.balance + money

    #Player deduct money (Loses bet)
    def deduct_money(self,money):
        if type(money)!=int:
            print("This is not money")
        else:
            self.balance = self.balance - money
    
    def __str__(self):
        return f"Player: {self.name} Balance: {self.balance}"

def check_bust(cards_list, turn):
    total = 0 #Ace counts as 11
    total_A = 0 #Ace counts as 1
    for item in cards_list:
        if item.rank == "Ace":
            total += item.value
            total_A += 1
        #If no ACE, these two value should be the same
        else:
            total += item.value
            total_A += item.value
    
    #If two options aren't busted, pick the one that is closest to 21
    if total<=21 and total_A<=21:
        if abs(total-21)<abs(total_A-21):
            print(f"{turn} Total value: {total}")
            return (True,total)
        else:
            print(f"{turn} Total value: {total_A}")
            return (True,total_A)
    #If ACE counts as 11 and bust, then return ACE counts as 1 if not busted
    elif total>21 and total_A<=21:
            print(f"{turn} Total value: {total_A}")
            return (True,total_A)
    #Return False to end the round since the player bust
    else:
        print(f"{turn} Total value: {total_A}! {turn} BUST!")
        return (False,total_A)

def show_some(turn, card_list):
    print(f"\n{turn}'s hand: ")
    print(" <Hidden>")
    print(card_list[1])

def show_all(turn, card_list):
    print(f"\n{turn}'s Hand:",*card_list, sep='\n ')

#This should be checked everytime cards is dealt from the deck
def check_running_count(cards):
    global count #Modify the count directly
    #This return True if the cards is only passed in one card
    if isinstance(cards,Card):
        count += cards.count
    #It should only goes here if count is passed in a list
    else:
        for item in cards:
            count += item.count

#GAME LOGIC

#GAME SETUP
intro()
#It creates a deck of card
deck = Deck()
deck.create_new_deck()
#Shuffles the card
deck.shuffle()
#Hi-Lo Running count
count = 0

name = input("Please Enter Your Name: ")
Balance = int(input("Please Add Money to Your Balance: "))
player = Player(name,Balance)
print(player)
print("------------------GAME START-------------------")

#It falls into this loop whenever a new round has started
while True:

    #New round Setup
    #Player places their bet
    print(f"\nCount: {count}")
    bet = int(input("Please places your bet: "))
    while player.bet(bet)==NULL:
        bet = int(input("Please places your bet: "))
    
    #Setup for lists of card that player and dealer have on the table
    player_cards = []
    dealer_cards = []
    player_total = 0
    dealer_total = 0

    #Before dealing cards, check if the deck has enough cards
    deck.check_deck()
    #Deals two cards to the Dealer and the player
    for i in range(2):
        dealer_cards.append(deck.deal_one())
        player_cards.append(deck.deal_one())
    
    #Shows Dealer's hand
    show_some("Dealer", dealer_cards)
    check_running_count(dealer_cards[1])

    #Shows Player's Hand
    show_all(name, player_cards)
    check_running_count(player_cards)

    same_round = True
    turn = name

    while same_round:
        #Player's turn
        if turn == name:   
            
            #it won't bust at this point, it will print the player's total value
            same_round = check_bust(player_cards, turn)

            hit_stand = True
            
            #Goes into a loop of hit or stand until the player chooses Stand or Double Down
            while hit_stand and same_round:
                action = input(f"Would you want to HIT(H), STAND(S), or Double Down(DD), Count = {count}: ").lower()

                while action!="h" and action!="s" and action!="dd":
                    action = input(f"Would you want to HIT or STAND (H,S), Count = {count}: ").lower()
                
                #Player hits
                if action == "h":
                    player_cards.append(deck.deal_one())
                    check_running_count(player_cards[-1])

                    #Print player's card
                    show_all(name, player_cards)

                    #Check player total value, Check if player busts or not
                    (same_round, player_total) = check_bust(player_cards, turn)
                
                #Player doubles down
                elif action == "dd":
                    #End the hit_stand loop, Dealer's turn
                    hit_stand = False
                    turn = "Dealer"

                    #Doubles the bet
                    bet = bet*2
                    print(f"Bet has been doubled! Bet: {bet}")

                    player_cards.append(deck.deal_one())
                    check_running_count(player_cards[-1])

                    #Print player's card
                    show_all(name, player_cards)

                    #Check player total value, Check if player busts or not
                    (same_round, player_total) = check_bust(player_cards, turn)
                    

                #Player chooses stand
                else:
                    #End the hit_stand loop, Dealer's turn
                    hit_stand = False
                    turn = "Dealer"

                    #Print Player's card
                    show_all(name, player_cards)

                    #Check player total value, Check if player busts or not
                    (same_round, player_total) = check_bust(player_cards, turn)
        
        #If the player hasn't busted, dealer's turn
        #if same_round = False --> Player busted > Dealer doesn't have to take his turn
        elif turn == "Dealer" and same_round == True:
            #Print dealer's hand, it reveals dealer's first card
            show_all("Dealer", dealer_cards)
            check_running_count(dealer_cards[0])
            #It won't bust, but it will print out the total value
            (same_round, dealer_total) = check_bust(dealer_cards, turn)
            while dealer_total<17 or dealer_total<player_total:
                dealer_cards.append(deck.deal_one())
                check_running_count(dealer_cards[-1])
                #Print dealer's hand
                show_all("Dealer", dealer_cards)
                #Check the total value everytime the dealer hits
                (same_round, dealer_total) = check_bust(dealer_cards, turn)
                if same_round == False or dealer_total>=player_total:
                    break

        #It goes here everytime Dealer or Player ends their turn
        #If someone BUST or dealer_total>=player_total it ends this round
        if same_round == False or dealer_total>=player_total:
            break
                

    #Check if player wins the bet or not
    #Lose bet
    if player_total>21 or (player_total<=21 and dealer_total<=21 and dealer_total>player_total):
        player.deduct_money(bet)
        print(f"\nDeduct money: {bet}")
    #Win bet
    elif dealer_total>21 or (player_total<=21 and dealer_total <= 21 and player_total>dealer_total):
        player.add_money(bet)
        print(f"\nAdd money: {bet}") 
    
    elif player_total == dealer_total:
        print("\nIt's a tie. You don't win or lose the bet")

    
    #Print the balance for the user
    print(player)

    #Check if the player has 0 balance
    if player.balance <= 0:
        print("\nYou're bankrupt")
        break
    
    #Check if player wants to keeps playing
    gameon = "default"
    while gameon!="y" and gameon!="n":
        gameon = input("Would you like to play another hand (Y/N): ").lower()
    
    if gameon == "y":
        pass
    else:
        break

        

    
        
    





