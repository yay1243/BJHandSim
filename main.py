import random
import numpy as np
from collections import Counter

HIT = 0
STAY = 1
WIN = 1
LOSE_TIE = 0


def new_round(players, deck, rigged=False):
    for hand in players:
        hand.clear()
    if rigged:
        return True
    for a in range(2):
        for hand in players:
            hand.append(draw(deck))
    for id_hand, hand in enumerate(players):
        if point_value(hand) == 21:
            return id_hand
    return True


def dealer_routine(hand, deck):
    while point_value(hand) < 16:
        hand.append(draw(deck))
    return point_value(hand)


def player_random_routine(hand, deck):
    actions = []
    while point_value(hand) < 18:
        if random.randint(0, 1) == 0:
            actions.append(HIT)
            hand.append(draw(deck))
        else:
            actions.append(STAY)
            break
    return actions


def draw(deck):
    top_card = deck[0]
    deck.pop(0)
    return top_card


def rig_hand(deck, hand, value):
    # Only rigs for hard values as of now tehe :P
    if value < 12:
        hand.append(random.randint(2, value-1))
        hand.append(value-hand[0])
    elif value == 21:
        hand.append(1)
        hand.append(10)
    else:
        for a in range(2,11):
            if (value-a) == 10:
                minimum = a
        hand.append(random.randint(minimum,10))
        hand.append(value-hand[0])
    deck.remove(hand[0])
    deck.remove(hand[1])
    random.shuffle(deck)
    return True


def rig_upcard(deck, hand, value):
    hand.append(value)
    deck.remove(value)
    random.shuffle(deck)
    hand.append(draw(deck))
    return True


def fill_shoe(no_of_decks):
    deck = [1,2,3,4,5,6,7,8,9,10,10,10,10] * 4 * no_of_decks
    return deck


def point_value(hand):
    soft = 0
    hard = sum(hand)
    if 1 in hand:
        soft = hard + 10
    if hard < soft <= 21:
        return soft
    else:
        return hard


def round_result(players):
    dealer = point_value(players[0])
    player = point_value(players[1])
    if player > 21:
        return LOSE_TIE
    if dealer > 21:
        return WIN
    if dealer >= player:
        return LOSE_TIE
    else:
        return WIN


if __name__ == '__main__':
    dealer, player_1 = [], []
    wins = 0
    action_chart = np.zeros((2,5,10), dtype=np.uint32)
    # [WIN/LOSE][Hard Total][Dealer upcard]
    print(action_chart)
    action_chart[0][1][2] = 4
    print(action_chart)
    for a in range(100000):
        players = [dealer, player_1]
        deck = fill_shoe(1)
        new_round(players, deck, True)
        rig_hand(deck, player_1, 20)
        rig_upcard(deck, dealer, 5)
        player_1.append(draw(deck))
        dealer_routine(dealer, deck)
        if round_result([dealer, player_1]) == WIN:
            wins += 1
            #print(point_value(dealer), point_value(player_1))
    a += 1
    print(wins)
    print("Win Percent chance = " + str(wins / a))



