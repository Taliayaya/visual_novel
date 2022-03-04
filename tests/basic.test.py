#!/usr/bin/env python3
from visual_novel.interpreter import getChoices
import unittest


class BasicTests(unittest.TestCase):
    def test_getChoices(self):
        testTxt = '#No~dewit.txt|...~tragedy.txt$'
        expectOutput = {"type":"choice", "choice1":('No', 'dewit.txt'), "choice2": ('...', 'tragedy.txt')}
        result = getChoices(testTxt)
        self.assertDictEqual(result, expectOutput)


if __name__ == "__main__":
    unittest.main()

