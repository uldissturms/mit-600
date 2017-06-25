from fifth_ghost import *

def test_valid_input():
    assert valid_input('a') == True
    assert valid_input('1') == False

def test_is_long_enough_to_lose():
    assert is_long_enough_to_lose('abc') == False
    assert is_long_enough_to_lose('abcde') == True

def test_is_a_word():
    assert is_a_word(['bye'], 'bye') == True
    assert is_a_word(['bye'], 'none') == False

def test_begins_with():
    assert begins_with(['bye'], 'by') == True
    assert begins_with(['bye'], 'ye') == False

def test_next_player():
    assert next_player(1) == 2
    assert next_player(2) == 1
