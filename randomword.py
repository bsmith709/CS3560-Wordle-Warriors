import random

# Create empty list to store valid words
valid_words = []

# Opens txt file in read mode
# "with" ensures that file closes after reading
with open('wordlist.txt' , 'r') as file: 
    # Removes leading and trailing whitespaces and converts words to lower (implemented to work with any list file)
    valid_words = [word.strip().lower() for word in file.readlines()]

# Chooses a random word from the list
correct_word = random.choice(valid_words)

while True:
    # Converts user input to lowercase for comparison
    user_input = input("Enter your guess: ").lower()

    if user_input in valid_words:
        break
    else:
        print("Invalid guess. Please enter a valid word.")

    wordle_game = wordleWord(user_input, correct_word)

    if user_input == correct_word:
        print("You've guessed the correct word!")
        break
    else:
        worde_game.print()
