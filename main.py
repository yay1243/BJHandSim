import random
import numpy as np
import os.path

HIT = 0
STAND = 1
WIN = 1
TIE = 0
LOSE = -1


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
    while point_value(hand) < 17:
        hand.append(draw(deck))
    return point_value(hand)


def player_random_routine(hand, deck):
    actions = []
    while point_value(hand) < 18:
        if random.randint(0, 1) == 0:
            actions.append(HIT)
            hand.append(draw(deck))
        else:
            actions.append(STAND)
            break
    return actions


def player_routine(dealer, player, deck, rec_actions):
    standing = False
    while not standing:
        try:
            rec_action = rec_actions[dealer[0]][point_value(player)]
            if rec_action == HIT:
                player.append(draw(deck))
            else:
                standing = True
        except IndexError:
            standing = True
    return True


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


def round_result(dealer, player):
    dealer_value = point_value(dealer)
    player_value = point_value(player)
    if player_value > 21:
        return LOSE
    if dealer_value > 21:
        return WIN
    if dealer_value > player_value:
        return LOSE
    if dealer_value == player_value:
        return TIE
    else:
        return WIN


if __name__ == '__main__':
    dealer, player_1 = [], []
    hard_win_prob = np.zeros((2, 10, 10), dtype=np.int32)
    # [WIN/LOSE][Hard Total][Dealer upcard]
    # if os.path.isfile('./flat_hard_win_prob.npy'):
    #     flat_hard_win_prob = np.load('flat_hard_win_prob.npy')
    #     hard_win_prob = flat_hard_win_prob.reshape((hard_win_prob.shape[0], hard_win_prob.shape[1],
    #                                                 hard_win_prob.shape[2]))
    # np.save('flat_hard_win_prob', hard_win_prob)
    players = [dealer, player_1]
    rec_action_table = np.zeros((10,10), dtype=np.int32)
    win_differential = np.zeros((10,10), dtype=np.int32)
    for a in range(rec_action_table.shape[1]):
        rec_action_table[9][a] = 1
    for player_value in range(9, -1, -1):
        for dealer_upcard in range(10):
            for action in [HIT, STAND]:
                for a in range(10000):
                    deck = fill_shoe(1)
                    new_round(players, deck, True)
                    rig_hand(deck, player_1, player_value+8)
                    rig_upcard(deck, dealer, dealer_upcard+1)
                    if action == HIT:
                        player_1.append(draw(deck))
                        player_routine(dealer, player_1, deck, rec_action_table)
                    dealer_routine(dealer, deck)
                    hard_win_prob[action][player_value][dealer_upcard] += round_result(dealer, player_1)
            if hard_win_prob[HIT][player_value][dealer_upcard] > hard_win_prob[STAND][player_value][dealer_upcard]:
                rec_action_table[player_value][dealer_upcard] = HIT
                win_differential[player_value][dealer_upcard] = hard_win_prob[HIT][player_value][dealer_upcard]
            else:
                rec_action_table[player_value][dealer_upcard] = STAND
                win_differential[player_value][dealer_upcard] = hard_win_prob[STAND][player_value][dealer_upcard]
    print(hard_win_prob)
    print(rec_action_table)
    print(win_differential)

