 
# import random , itertools 
# deck = list(itertools.product(range(1,14),["Spade","Club","Hearts","Diamond"]))
# random.Suffle(deck)
# print(deck)
# for i in range(5):
#      print(deck[i][0],"of",deck[i][1])

#same program

# import random
# import itertools

# # Create a deck of cards
# deck = list(itertools.product(range(1, 14), ["spade", "club", "hearts", "diamond"]))

# # Shuffle the deck
# random.shuffle(deck)

# # Print the shuffled deck (optional)
# print("Shuffled deck:", deck)

# # Deal 5 cards
# print("Dealt cards:")
# for i in range(5):
#     print(deck[i][0], "of", deck[i][1])

#same program

import random,itertools
#import itertools

# Create a deck of cards
deck = list(itertools.product(range(1, 14), ["spade", "club", "hearts", "diamond"]))

# Shuffle the deck
random.shuffle(deck)  # Correct spelling of shuffle

# Print the shuffled deck (optional)
print(deck)

# Deal 5 cards
for i in range(5):
    print(deck[i][0], "of", deck[i][1])

