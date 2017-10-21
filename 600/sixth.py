# Problem Set 5: 6.00 Word Game

import random
import string
from time import *

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq


# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def add_bonus_if_earned(word, n, score):
    return score + 50 if len(word) == n else score

def score_a_word(word):
    return sum([SCRABBLE_LETTER_VALUES[c] for c in word])

def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    The score for a word is the sum of the points for letters
    in the word, plus 50 points if all n letters are used on
    the first go.

    Letters are scored as in Scrabble; A is worth 1, B is
    worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string (lowercase letters)
    returns: int >= 0
    """
    return add_bonus_if_earned(word, n, score_a_word(word))

#
# Make sure you understand how this function works and what it does
#

def flatten(list):
    return [item for sublist in list for item in sublist]

def dict_to_sorted_list(dict):
    return flatten([[key] * dict[key] for key in sorted(dict.keys())])

def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    return ' '.join(dict_to_sorted_list(hand))

#
# Make sure you understand how this function works and what it does!
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    At least n/3 the letters in the hand should be VOWELS.

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    hand={}
    num_vowels = n / 3

    for i in range(num_vowels):
        x = VOWELS[random.randrange(0,len(VOWELS))]
        hand[x] = hand.get(x, 0) + 1

    for i in range(num_vowels, n):
        x = CONSONANTS[random.randrange(0,len(CONSONANTS))]
        hand[x] = hand.get(x, 0) + 1

    return hand

#
# Problem #2: Update a hand by removing letters
#
def remove_empty(dict):
    return {k:dict[k] for k in dict.keys() if dict[k] != 0}

def substract(dict, list):
    new_dict = dict.copy()
    for item in list:
        if item in new_dict:
            new_dict[item] -= 1
        else:
            new_dict[item] = -1
    return new_dict

def update_hand(hand, word):
    """
    Assumes that 'hand' has all the letters in word.
    In other words, this assumes that however many times
    a letter appears in 'word', 'hand' has at least as
    many of that letter in it. 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not mutate hand.

    word: string
    hand: dictionary (string -> int)
    returns: dictionary (string -> int)
    """
    return remove_empty(substract(hand, list(word)))


#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, scored_word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.

    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    """
    if word not in scored_word_list:
        return False
    diff = substract(hand, word)

    return all(v >= 0 for v in diff.values())

#
# Problem #4: Playing a hand
#
def adjust_for_time_taken(score, time):
    return score if time < 1 else round(score / time, 2)

def prompt_for_a_word():
    return raw_input('Enter word, or a . to indicate that you are finished:')

# w - words in list
# l - length of the longest word in list, expected to be > h
# h - letters in hand

# O(w*l+wlogw)
def pick_best_word(hand, scored_word_list):

    options = {word:scored_word_list[word] for word in scored_word_list.keys() if is_valid_word(word, hand, scored_word_list)}

    return (sorted(options, key=options.get, reverse=True) or ['.'])[0]

# O(h^2)
def pick_best_word_faster(hand, rearranged_word_list):
    sorted_hand = ''.join(dict_to_sorted_list(hand))
    length = len(sorted_hand)

    for size in range(length, 0, -1):
        for offset in range(0, length - size + 1):
            candidate = sorted_hand[offset:(size + offset)]
            if candidate in rearranged_word_list:
                return rearranged_word_list[candidate]

    return '.'

def get_time_limit(scored_word_list, k):
    start_time = time()
    for word in scored_word_list:
        get_frequency_dict(word)
        get_word_score(word, HAND_SIZE)
    return (time() - start_time) * k

def play_hand(hand, scored_word_list, rearranged_word_list, total_time, time_left, total = 0):
    print('Current Hand:', display_hand(hand))
    start_time = time()
    word = pick_best_word_faster(hand, rearranged_word_list)
    time_taken = time() - start_time
    print('It took {:.2f} seconds to provide an answer'.format(time_taken))

    time_left -= time_taken
    if (time_left <= 0):
        print('Total time exceeds {}. You scored {} points.'.format(total_time, total))
        return

    print('You have {:.2f} seconds remaining'.format(time_left))

    if word == '.':
        print('Total score: %s points' % total)
        return

    if not is_valid_word(word, hand, scored_word_list):
        print('%s is not a valid word' % word)
        return play_hand(hand, scored_word_list, rearranged_word_list, total_time, time_left, total)

    score = adjust_for_time_taken(get_word_score(word, HAND_SIZE), time_taken)
    total += score

    print('%s earned %s points. Total: %s points' % (word, score, total))
    return play_hand(update_hand(hand, word), scored_word_list, rearranged_word_list, total_time, time_left, total)

#
# Problem #5: Playing a game
# Make sure you understand how this code works!
#

def prompt_for_total_time():
    return int(raw_input('Enter time limit, in seconds, for players:'))

def get_words_to_points(word_list):
    return {word:score_a_word(word) for word in word_list}

def get_word_rearrangements(word_list):
    return {''.join(sorted(word)):word for word in word_list}

def play_game(word_list):
    """
    Allow the user to play an arbitrary number of hands.

    * Asks the user to input 'n' or 'r' or 'e'.

    * If the user inputs 'n', let the user play a new (random) hand.
      When done playing the hand, ask the 'n' or 'e' question again.

    * If the user inputs 'r', let the user play the last hand again.

    * If the user inputs 'e', exit the game.

    * If the user inputs anything else, ask them again.
    """
    scored_word_list = get_words_to_points(word_list)
    rearranged_word_list = get_word_rearrangements(word_list)

    while True:
        cmd = raw_input('Enter n to deal a new hand, r to replay the last hand, or e to end game: ')
        if cmd == 'n':
            total_time = prompt_for_total_time()
            hand = deal_hand(HAND_SIZE)
            play_hand(hand.copy(), scored_word_list, rearranged_word_list, total_time, total_time)
            print()
        elif cmd == 'r':
            total_time = prompt_for_total_time()
            play_hand(hand.copy(), scored_word_list, rearranged_word_list, total_time, total_time)
            print()
        elif cmd == 'e':
            break
        else:
            print("Invalid command.")

#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
