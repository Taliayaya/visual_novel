from visual_novel.interpreter import getChoices
import unittest


class BasicTests(unittest.TestCase):
    def basicTestChoices(self):
        testTxt = '#No~dewit.txt|...~tragedy.txt$'
        expectOutput = [('No', 'dewit.txt'), ('...', 'tragedy.txt')]
        result = getChoices(testTxt)
        self.assertListEqual(result, expectOutput)


if __name__ == "__main__":
    unittest.main()
