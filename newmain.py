import pygame
import random
import time
from sys import exit

# Opens txt file in read mode
# "with" ensures that file closes after reading
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

# List of named colors in pygame: https://www.pygame.org/docs/ref/color_list.html

# Initialize the pygame module
pygame.init()

# Initialize the display area
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Wordle")
screen.fill('gray26')

# Initialize the game clock to control FPS
clock = pygame.time.Clock()

# 'Surfaces' are images that can be displayed using the blit() function
width = 80
height = 80
correct_surface = pygame.Surface((width, height))
correct_surface.fill('green')
partially_correct_surface = pygame.Surface((width, height))
partially_correct_surface.fill('orange')
incorrect_surface = pygame.Surface((width, height))
incorrect_surface.fill('gray')

# Loading a surface from an image
filePath = 'assets/square.png'
example_surface2 = pygame.image.load(filePath)

# Creating a text surface
font_type = None
font_size = 100
example_font = pygame.font.Font(font_type, font_size)


def displayWords(guesses, correct):
    x_cord = 120
    y_cord = 100
    row = 0
    for guess in guesses:
        row += 1
        column = 0
        i = 0
        for letter in guess:
            column += 1
            text = example_font.render(letter, False, 'black')
            if letter == correct[i]:
                screen.blit(correct_surface, (x_cord * column, y_cord * row))
            elif letter in correct:
                screen.blit(partially_correct_surface, (x_cord * column, y_cord * row))
            else:
                screen.blit(incorrect_surface, (x_cord * column, y_cord * row))
            i += 1
            screen.blit(text, (x_cord * column, y_cord * row))

def displayGuess(guess, row):
    x_cord = 120
    y_cord = 100 + (100 * row)
    column = 0
    for letter in guess:
        column += 1
        text = example_font.render(letter, False, 'black')
        screen.blit(incorrect_surface, (x_cord * column, y_cord))
        screen.blit(text, (x_cord * column, y_cord))


if __name__ == "__main__":
    guesses = []
    guess = ""
    correct_word = randomword(valid_solutions)

    # Main game loop
    while True:

        screen.fill('gray26')
        # This is the event loop it checks for any player input
        for event in pygame.event.get():
            # This means the user pressed a key, this is where all of our letter inputs are handled
            if event.type == pygame.KEYDOWN:

                if len(guess) < 5:
                    if event.key == pygame.K_a: # K_a is the constant for the 'a' key, the rest of the constants are at https://www.pygame.org/docs/ref/key.html
                        guess += "a"
                    if event.key == pygame.K_b:
                        guess += "b" 
                    if event.key == pygame.K_c:
                        guess += "c"
                    if event.key == pygame.K_d:
                        guess += "d"
                    if event.key == pygame.K_e:
                        guess += "e"
                    if event.key == pygame.K_f:
                        guess += "f"
                    if event.key == pygame.K_g:
                        guess += "g"
                    if event.key == pygame.K_h:
                        guess += "h"
                    if event.key == pygame.K_i:
                        guess += "i"
                    if event.key == pygame.K_j:
                        guess += "j"
                    if event.key == pygame.K_k:
                        guess += "k"
                    if event.key == pygame.K_l:
                        guess += "l" 
                    if event.key == pygame.K_m:
                        guess += "m"
                    if event.key == pygame.K_n:
                        guess += "n"
                    if event.key == pygame.K_o:
                        guess += "o"
                    if event.key == pygame.K_p:
                        guess += "p"
                    if event.key == pygame.K_q:
                        guess += "q"
                    if event.key == pygame.K_r:
                        guess += "r"
                    if event.key == pygame.K_s: 
                        guess += "s"
                    if event.key == pygame.K_t: 
                        guess += "t"
                    if event.key == pygame.K_u: 
                        guess += "u"
                    if event.key == pygame.K_v: 
                        guess += "v"
                    if event.key == pygame.K_w: 
                        guess += "w"
                    if event.key == pygame.K_x: 
                        guess += "x"
                    if event.key == pygame.K_y: 
                        guess += "y"
                    if event.key == pygame.K_z: 
                        guess += "z"

                if event.key == pygame.K_BACKSPACE: 
                    guess = guess[0:-1]

                # This means user hit the enter key which should mean they typed a word and need it checked
                if event.key == pygame.K_RETURN: 
                    if guess in valid_words:
                        guesses.append(guess)
                        guess = ""
                    pass

            # This means the user closed the window
            if event.type == pygame.QUIT:
                # Terminates the program
                pygame.quit()
                exit()


        
        # The blit() function displays a surface at a specified coordinate
        # coords = (0,0)
        # screen.blit(example_surface2, coords)

        # Display guesses and current word being typed
        displayWords(guesses, correct_word)
        displayGuess(guess, len(guesses))

        # Updates the display with all new objects
        pygame.display.update()

        #Sets the maximum number of iterations for the while loop per second
        clock.tick(60)