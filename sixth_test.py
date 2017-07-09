from sixth import *

def test_dict_to_sorted_list():
    assert dict_to_sorted_list({'a': 2, 'b': 1}) == ['a', 'a', 'b']

def test_display_hand():
    assert display_hand({'a': 1, 'x': 2}) == 'a x x'

def test_adjust_for_time_taken():
    assert adjust_for_time_taken(10, 0) == 10
    assert adjust_for_time_taken(10, 2) == 5
    assert adjust_for_time_taken(10, 1.25) == 8
    assert adjust_for_time_taken(10, 3.33) == 3.00
    assert adjust_for_time_taken(10, 0.01) == 10

def test_get_words_to_points():
    assert get_words_to_points(['abc']) == {'abc': 7}
    assert get_words_to_points(['abc', 'ab']) == {'abc': 7, 'ab': 4}

def test_substract():
    assert substract({'a': 1, 'b': 2}, ['a', 'b', 'c']) == {'a': 0, 'b': 1, 'c': -1}

def test_pick_best_word():
    assert pick_best_word({'a': 1}, {}) == '.'
    assert pick_best_word({'a': 2, 'w': 1, 'y': 1}, {'way': 1, 'away': 2}) == 'away'

def test_get_time_limit():
    word_list = load_words()
    scored_word_list = get_words_to_points(word_list)
    assert get_time_limit(scored_word_list, 10) > 3

def test_get_word_rearrangements():
    assert get_word_rearrangements(['way', 'away']) == {'aawy': 'away', 'awy': 'way'}

def test_pick_best_word_faster():
    assert pick_best_word_faster({'a': 2, 'w': 1, 'y': 1}, {'awy': 'way', 'aawy': 'away'}) == 'away'
    assert pick_best_word_faster({'a': 2, 'w': 1, 'y': 2}, {'awy': 'way'}) == 'way'
    assert pick_best_word_faster({'a': 1, 'w': 1}, {'awy': 'way'}) == '.'

hand = {'a': 3, 'c': 2, 'e': 1, 'd': 1}
word_list = load_words()
scored_word_list = get_words_to_points(word_list)
rearranged_word_list = get_word_rearrangements(word_list)

def test_time_pick_best_word():
    start_time = clock()
    pick_best_word(hand, scored_word_list)
    assert (clock() - start_time) < 0.5

def test_time_pick_best_word_faster():
    start_time = clock()
    pick_best_word_faster(hand, rearranged_word_list)
    assert (clock() - start_time) < 0.0001
