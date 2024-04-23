import unittest
from unittest.mock import patch
from snippet import randomword

class TestRandomWord(unittest.TestCase):
    
    def test_randomword_with_valid_list(self):
        wordlist = ["here", "there", "anywhere", "everywhere", "nowhere"]
        selected_word = randomword(wordlist)
        self.assertIn(selected_word, wordlist, "Selected word should be present in the word list")

    def test_randomword_with_empty_list(self):
        wordlist = []
        with self.assertRaises(IndexError):
            randomword(wordlist)

    def test_randomword_with_one_word(self):
        wordlist = ["hello"]
        selected_word = randomword(wordlist)
        self.assertEqual(selected_word, "hello", "Selected word should be 'hello'")

if __name__ == '__main__':
    unittest.main()
    
    