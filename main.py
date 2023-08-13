import random

HIT = 0
STAY = 1
WIN = 1
LOSE_TIE = 0

def new_round(players, deck):
    for hand in players:
        hand.clear()
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


def player_random_routine(hand, deck, actions):
    while point_value(hand) < 18:
        if random.randint(0, 1) == 0:
            actions.append(HIT)
            hand.append(draw(deck))
        else:
            actions.append(STAY)
            break
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
    return True


def rig_upcard(deck, hand, value):
    hand.append(value)
    hand.append(draw(deck))
    deck.remove(hand[0])
    return True


def shuffle_deck(deck_number):
    deck = [1,2,3,4,5,6,7,8,9,10,10,10,10] * 4 * deck_number
    random.shuffle(deck)
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


def update_win_chart(dealer, player, actions, outcome, chart):
    # chart[action][dealer up card][hard value]
    if len(player) > 2:
        player.pop()
    for action in reversed(actions):
        if action == HIT:
            chart[HIT][dealer[0]][point_value(player)].append(outcome)
        else:
            chart[STAY][dealer[0]][point_value(player)].append(outcome)
    return True


if __name__ == '__main__':
    dealer, player_1 = [], []
    shuffled = shuffle_deck(1)
    print(shuffled)
    rig_upcard(shuffled, dealer, 3)
    print(dealer)
    rig_hand(shuffled, player_1, 20)
    print(shuffled)
    print(player_1)
    # for a in range(2):
    #     players = [dealer, player_1]
    #     new_round(players, shuffled)
    #     print(dealer, player_1)
    #     print(shuffled)

