import random
import card

def evaluate_rarity(value):
    #bar, grape, lemon
    if value in [1,22,43]:
        return random.randint(3,4)
    #7
    if value == 64:
        return 5
    #pair
    if value in [2,3,4,6,11,16,17,21,23,24,27,32,33,38,41,42,44,48,49,54,59,61,62,63]:
        return random.randint(1,2)
    
    return 0

def generate_card_id(dice):
    rarity = evaluate_rarity(dice)
    if not(rarity): return 0
    last = card.read_by_rarity(rarity)
    print(last)
    #define the card
    return last[random.randint(0,len(last)-1)]