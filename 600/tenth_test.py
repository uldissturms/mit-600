from tenth import *

def test_update_hand():
    hand = Hand(4, {'a': 2, 'w': 1, 'y': 1})
    hand.update('way')
    assert hand == Hand(1, {'a':1})

def test_hand_contains_letters():
    hand = Hand(4, {'a': 2, 'w': 1, 'y': 1})
    assert hand.containsLetters('way') == True
    assert hand.containsLetters('away') == True
    assert hand.containsLetters('noaway') == False

def test_empty_hand():
    assert Hand(4, {}).isEmpty() == True
    assert Hand(4, {'a': 1}).isEmpty() == False

def test_player_comparison():
    player1 = Player(1, {})
    player1.addPoints(1)

    player2 = Player(2, {})
    player2.addPoints(2)

    assert player1 < player2

def test_wordlist_scores_words():
    scored_list = Wordlist().getScoredList()
    assert scored_list['away'] == 10
    assert scored_list['way'] == 9

def test_computer_player_can_pick_the_best_word():
    computer = ComputerPlayer(1, Hand(4, {'a': 2, 'w': 1, 'y': 1}))
    wordlist = Wordlist()
    assert computer.pickBestWord(wordlist) == 'away'
