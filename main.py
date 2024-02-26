import random

# Opens txt file in read mode
# "with" ensures that file closes after reading
with open('wordlist.txt', 'r') as file:
    # Removes leading and trailing whitespaces and converts words to lower (implemented to work with any list file)
    valid_words = [word.strip().lower() for word in file.readlines()]

# Picks a random word
def randomword(wordlist):
    # Chooses a random word from the list
    correct_word = random.choice(wordlist)
    return correct_word

# Color variables
class colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    END = '\033[0m'

# Letter class
class wordleLetter:
    char = ""
    color = ""
    def __init__(self, ch, clr):
        self.char = ch
        self.color = clr
    
    def __str__(self):
        return self.char

class wordleWord:

    # Constructor for a wordleWord
    # To call it use wordleWord(str, correct_word)
    # str - The word guessed by the user
    # correct_word - The word that the user needs to guess
    def __init__(self, str, correct_word):
        self.word = []
        for i in range(5):
            if str[i] == correct_word[i]:
                self.word.append(wordleLetter(str[i], "green"))
            elif str[i] in correct_word:
                self.word.append(wordleLetter(str[i], "yellow"))
            else:
                self.word.append(wordleLetter(str[i], "gray"))
    
    # Print function for a wordleWord that prints each letter in the correct color
    # To call it use word.print() with the word variable being a wordleWord
    def print(self):
        for letter in self.word:
            if letter.color == "gray":
                print(letter, end="")
            elif letter.color == "yellow":
                print(colors.YELLOW + str(letter) + colors.END, end="")
            else:
                print(colors.GREEN + str(letter) + colors.END, end="")
        print()


if __name__ == "__main__":
    # Variables for number of guesses, list of guessed words, and game state; False = still going, True = game done
    numguesses = 6
    guesses = []
    done = False

    # Stub for correct_word, actual variable needs to be implemented from randomword
    correct = randomword(valid_words)

    def getWord():
        word = input("Guess: ")
        if word.lower() in valid_words:
            return word
        else:
            print("Invalid word")
            return getWord()

    # Game loop
    while numguesses > 0 and not done:
        guess = wordleWord(getWord(), correct)
        guess.print()
        # Logic for checking word needs to be implemented here

        guesses.append(guess)
        numguesses -= 1


