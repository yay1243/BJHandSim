import random


def dealer_routine():
    return True


def draw(deck):
    top_card = deck[0]
    deck.pop(0)
    return top_card


def shuffle_deck(deck_number):
    deck = [1,2,3,4,5,6,7,8,9,10,10,10,10] * 4 * deck_number
    random.shuffle(deck)
    return deck


def point_value(hand):
    soft = 0
    hard = sum(hand)
    if 1 in hand:
        soft = hard + 10
    print(soft, hard)
    if hard < soft <= 21:
        return soft
    else:
        return hard


if __name__ == '__main__':
    print(point_value([1,9,1,2]))
    shuffled = shuffle_deck(1)
    print(shuffled)
    print(draw(shuffled))
    print(shuffled)

