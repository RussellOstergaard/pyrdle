import assignment09
import ciscTestCase
import unittest
from unittest.mock import patch
import sys
import io


class Assignment09Tests(ciscTestCase.CiscTestCase, unittest.TestCase):


    def test_pick_word(self):
        my_list = ['store', 'shore', 'snare', 'snort', 'stare', 'tries', 'rates', 'riots', 'story', 'tears']
        word = assignment09.pick_word(my_list)
        self.assertTrue(my_list.index(word) > -1, '\n\n*** pick_word problem: ' + word + ' is not in the word list ***\n')
        word2 = assignment09.pick_word(my_list)
        if word == word2:
            word2 = assignment09.pick_word(my_list)
        self.assertTrue(my_list.index(word) > -1 and word != word2, '\n\n*** pick_word problem: appears to be returning the same word each time ***\n')


    def test_generate_word_list(self):
        word_list = assignment09.generate_word_list()
        self.assertTrue(len(word_list) == 12972, '\n\n*** generate_word_list not reading and/or returning list of words correctly ***\n')


    def test_is_game_over(self):
        self.assertFalse(assignment09.is_game_over('tests', []), '\n\n*** is_game_over problem: not returning False without any guesses ***\n')
        self.assertTrue(assignment09.is_game_over('tests', ['estst', 'stste', 'tstes', 'stest', 'ttest', 'testt']), '\n\n*** is_game_over problem: not returning False with full list of 6 incorrect guesses ***\n')
        self.assertTrue(assignment09.is_game_over('tests', ['estst', 'stste', 'tstes', 'stest', 'ttest', 'tests']), '\n\n*** is_game_over problem: not returning True with correct answer in full guess list ***\n')
        self.assertTrue(assignment09.is_game_over('tests', ['tests']), '\n\n*** is_game_over problem: not returning True with correct answer in unfilled guess list ***\n')


    @patch("sys.stdin", io.StringIO('store\nfour\nsixsix\nnopee\nstore\n'))
    def test_get_guess(self):
        output = io.StringIO()
        sys.stdout = output

        guess = assignment09.get_guess(['store'])
        printed = output.getvalue().strip()
        self.assertTrue(guess == 'store', '\n\n*** get_guess problem: not returning valid guess ***\n')
        self.assertTrue(printed == 'Enter a guess:', '\n\n*** get_guess problem: not printing correct prompt to console ***\n')
        guess = assignment09.get_guess(['store'])
        printed = output.getvalue().strip()
        self.assertTrue(guess == 'store', '\n\n*** get_guess problem: not returning valid guess after invalid guesses ***\n')
        self.assertTrue(printed == 'Enter a guess: Enter a guess: Enter a guess: Enter a guess: Enter a guess:', '\n\n*** get_guess problem: not printing correct prompt to console when invalid guesses entered ***\n')


    def test_display_empty_board(self):
        output = io.StringIO()
        sys.stdout = output

        assignment09.display_board('snare', [])
        printed = output.getvalue().strip()
        expected = '+-----+\n|     |\n|     |\n|     |\n|     |\n|     |\n|     |\n+-----+'
        self.assertTrue(printed == expected, '\n\n*** display_board problem: empty board not printed correctly ***\n')


    def test_display_board_no_match(self):
        output = io.StringIO()
        sys.stdout = output

        assignment09.display_board('snare', ['lucky'])
        printed = output.getvalue().strip()
        expected = '+-----+\n|lucky|\n|     |\n|     |\n|     |\n|     |\n|     |\n+-----+'
        self.assertTrue(printed == expected, '\n\n*** display_board problem: not printing unmatched characters correctly ***\n')


    def test_display_board_with_yellow(self):
        output = io.StringIO()
        sys.stdout = output

        assignment09.display_board('snare', ['lucky','fails'])
        printed = output.getvalue().strip()
        expected = '+-----+\n|lucky|\n|f\033[93ma\033[0mil\033[93ms\033[0m|\n|     |\n|     |\n|     |\n|     |\n+-----+'
        self.assertTrue(printed == expected, '\n\n*** display_board problem: not identifying/printing yellow characters correctly ***\n')


    def test_display_board_with_green(self):
        output = io.StringIO()
        sys.stdout = output

        assignment09.display_board('snare', ['lucky','fails','scamp'])
        printed = output.getvalue().strip()
        expected = '+-----+\n|lucky|\n|f\033[93ma\033[0mil\033[93ms\033[0m|\n|\033[92ms\033[0mc\033[92ma\033[0mmp|\n|     |\n|     |\n|     |\n+-----+'
        self.assertTrue(printed == expected, '\n\n*** display_board problem: not identifying/printing green characters correctly ***\n')


    def test_display_board_complicated(self):
        output = io.StringIO()
        sys.stdout = output

        assignment09.display_board('poppy', ['poopy'])
        printed = output.getvalue().strip()
        expected = '+-----+\n|\033[92mp\033[0m\033[92mo\033[0mo\033[92mp\033[0m\033[92my\033[0m|\n|     |\n|     |\n|     |\n|     |\n|     |\n+-----+'
        self.assertTrue(printed == expected, '\n\n*** display_board problem: not identifying/printing complicated misplaced vs found characters correctly ***\n')


    def test_display_board_complicated_two(self):
        output = io.StringIO()
        sys.stdout = output

        assignment09.display_board('store', ['scene'])
        printed = output.getvalue().strip()
        expected = '+-----+\n|\033[92ms\033[0mcen\033[92me\033[0m|\n|     |\n|     |\n|     |\n|     |\n|     |\n+-----+'
        self.assertTrue(printed == expected, '\n\n*** display_board problem: not identifying/printing complicated misplaced vs found characters correctly ***\n')


    @patch("sys.stdin", io.StringIO('short\nshort\nshort\nshort\nshort\nshort\n'))
    def test_play_pyrdle_lose(self):
        output = io.StringIO()
        sys.stdout = output

        assignment09.play_pyrdle()
        printed = output.getvalue().strip()
        self.assertTrue(printed.startswith('PYRDLE'), '\n\n*** play_pyrdle problem: first printed line should be "PYRDLE" ***\n')
        self.assertTrue(printed.endswith('YOU LOSE'), '\n\n*** play_pyrdle problem: last printed line should be "YOU LOSE" ***\n')
        printed = printed.replace('YOU LOSE', '')
        printed = printed[:printed.rindex(':')]
        self.assertTrue(printed.endswith('The word was'), '\n\n*** play_pyrdle problem: second-to-last printed line should be "The word was: ___" ***\n')
        printed = printed.replace('\033[92m','')
        printed = printed.replace('\033[93m', '')
        printed = printed.replace('\033[0m', '')
        expected_content = '+-----+\n|short|\n|short|\n|short|\n|short|\n|short|\n|short|\n+-----+'
        self.assertTrue(printed.count(expected_content) > 0, '\n\n*** play_pyrdle problem: full board does not appear to print correctly" ***\n')