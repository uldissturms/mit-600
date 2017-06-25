from fifth import *

def test_get_word_score():
    assert get_word_score('', 7) == 0
    assert get_word_score('it', 7) == 2
    assert get_word_score('waybill', 7) == 65

def test_update_hand():
    assert update_hand({'a':1, 'q':1, 'l':2, 'm':1, 'u':1, 'i':1}, 'quail') == {'l':1, 'm':1}
    assert update_hand({'i':1, 's':1}, 'is') == {}

def test_is_valid_word():
    assert is_valid_word('hello', {'h':1, 'e':1, 'l':2, 'o':1}, ['hello']) == True
    assert is_valid_word('rapture', {'r': 1, 'a': 3, 'p': 2, 'e': 1, 't': 1, 'u':1}, ['rapture']) == False
    assert is_valid_word('honey', {'h': 1, 'o': 1, 'n': 1, 'e': 1, 'y':1}, []) == False
