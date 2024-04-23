import random

#Snippet from main before adding executable arguments

with open('wordlist.txt', 'r') as file:
    # Removes leading and trailing whitespaces and converts words to lower (implemented to work with any list file)
    valid_solutions = [word.strip().lower() for word in file.readlines()]
with open('valid-wordle-words.txt', 'r') as file:
    # Removes leading and trailing whitespaces and converts words to lower (implemented to work with any list file)
    valid_words = [word.strip().lower() for word in file.readlines()]

# Picks a random word
def randomword(wordlist):
    # Chooses a random word from the list
    correct_word = random.choice(wordlist)
    return correct_word