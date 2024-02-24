class colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    END = '\033[0m'

class wordleLetter:
    char = ""
    color = ""
    def __init__(self, ch, clr):
        self.char = ch
        self.color = clr
    
    def __str__(self):
        return self.char

class wordleWord:
    word = []

    def __init__(self, str, correct_word):
        for i in range(5):
            if str[i] == correct_word[i]:
                self.word.append(wordleLetter(str[i], "green"))
            elif str[i] in correct_word:
                self.word.append(wordleLetter(str[i], "yellow"))
            else:
                self.word.append(wordleLetter(str[i], "gray"))
    
    def print(self):
        for letter in self.word:
            if letter.color == "gray":
                print(letter, end="")
            elif letter.color == "yellow":
                print(colors.YELLOW + str(letter) + colors.END, end="")
            else:
                print(colors.GREEN + str(letter) + colors.END, end="")
        print()
