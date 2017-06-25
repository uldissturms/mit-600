# Problem Set 5: Ghost

import random

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)
import string

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r', 0)
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print "  ", len(wordlist), "words loaded."
    return wordlist

# (end of helper code)
# -----------------------------------

def valid_input(input):
    return input in string.ascii_letters

def is_long_enough_to_lose(word):
    return len(word) > 3

def is_a_word(word_list, word):
    return word in word_list

def begins_with(word_list, substring):
    return any(word.startswith(substring) for word in word_list)

def ghost():
    word_list = load_words()
    print 'Welcome to Ghost!'
    step('', word_list, 1)

def next_player(player):
    return (player % 2) + 1

def step(word, word_list, player):
    prev_player = next_player(player)
    print 'Current word fragment: \'%s\'' % word
    if is_long_enough_to_lose(word) and is_a_word(word_list, word):
        print 'Player %s loses because \'%s\' is a word.' % (prev_player, word)
        print 'Player %s wins!' % player
        return

    if not begins_with(word_list, word):
        print 'Player %s loses because no word begins with \'%s\'.' % (prev_player, word)
        print 'Player %s wins!' % player
        return

    letter = raw_input('Player %s\'s turn:' % player)
    if not valid_input(letter):
        print 'Not a letter: %s, please try again!' % letter
        return step(word, word_list, player)

    print 'Player %s says letter:', letter
    return step(word + letter.lower(), word_list, next_player(player))
