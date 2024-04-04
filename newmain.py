import random
from sys import exit
import pygame

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
#screen.fill('gray26')
screen.fill('aquamarine4')

logo_image = pygame.image.load('assets/newlogo.png')
logo_width = 375
logo_height = 75
logo_image = pygame.transform.scale(logo_image, (logo_width, logo_height))
logo_x = (SCREEN_WIDTH - logo_image.get_width()) // 2
logo_y = 3

bobcat_image = pygame.image.load('assets/bobcat.png')

restart_image = pygame.image.load('assets/restart.png')
quit_image = pygame.image.load('assets/quit.png')

#Restart Button
button_width = 50 
button_height = 50 
restart_button_x = 740
restart_button_y = 10

#End Restart Button
end_button_width = 200
end_button_height = 50
end_restart_button_x = (SCREEN_WIDTH - button_width) // 2
end_restart_button_y = SCREEN_HEIGHT / 2 + 50

#Quit Button
quit_button_width = 200
quit_button_height = 50
quit_button_x = (SCREEN_WIDTH - button_width) // 2
quit_button_y = SCREEN_HEIGHT / 2 + 125

restart_image = pygame.transform.scale(restart_image, (50, 47))
quit_image = pygame.transform.scale(quit_image, (50, 47))

# Initialize the game clock to control FPS
clock = pygame.time.Clock()

# 'Surfaces' are images that can be displayed using the blit() function
width = 80
height = 80
#correct_surface = pygame.Surface((width, height))
correct_surface = pygame.image.load('assets/correctSq.png')
#correct_surface.fill('green')
#partially_correct_surface = pygame.Surface((width, height))
partially_correct_surface = pygame.image.load('assets/partialSq.png')
#partially_correct_surface.fill('orange')
#incorrect_surface = pygame.Surface((width, height))
incorrect_surface = pygame.image.load('assets/incorrectSq.png')
#incorrect_surface.fill('gray')

# Loading a surface from an image
filePath = 'assets/square.png'
example_surface2 = pygame.image.load(filePath) #this goes for correct surface and etc

# Creating a text surface
font_type = None
font_size = 75
example_font = pygame.font.Font(font_type, font_size)

# Creating smaller sizes for the keyboard
smaller_width = 30
smaller_height = 30
unguessed_surface = pygame.Surface((smaller_width, smaller_height))
unguessed_surface.fill('white')
smaller_correct_surface = pygame.Surface((smaller_width, smaller_height))
smaller_correct_surface.fill((34,177,76))
smaller_partially_correct_surface = pygame.Surface((smaller_width, smaller_height))
smaller_partially_correct_surface.fill((255,207,93))
smaller_incorrect_surface = pygame.Surface((smaller_width, smaller_height))
smaller_incorrect_surface.fill('gray46')
smaller_font_size = 40
smaller_font = pygame.font.Font(font_type, smaller_font_size)

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

            square_center_x = x_cord * column + width / 2 #added
            # square_center_y = y_cord + height / 2 #parentheses?
            square_center_y = y_cord * row + height / 2 #parentheses?

            text = example_font.render(letter.upper(), False, 'white')
            text_width, text_height = example_font.size(letter.upper()) #added

            text_x = square_center_x - text_width / 2 #added
            text_y = square_center_y - text_height / 2

            #text = example_font.render(letter.upper(), False, 'black')

            if letter == correct[i]:
                screen.blit(correct_surface, (x_cord * column, y_cord * row))
            elif letter in correct:
                screen.blit(partially_correct_surface, (x_cord * column, y_cord * row))
            else:
                screen.blit(incorrect_surface, (x_cord * column, y_cord * row))
            i += 1
            #screen.blit(text, (x_cord * column, y_cord * row))
            screen.blit(text, (text_x, text_y)) #added * row

def displayGuess(guess, row):
    x_cord = 120
    y_cord = 100 + (100 * row)
    column = 0
    for letter in guess:
        column += 1

        square_center_x = x_cord * column + width / 2 #added
        square_center_y = y_cord + height / 2 #parentheses?

        text = example_font.render(letter.upper(), False, 'white')
        text_width, text_height = example_font.size(letter.upper()) #added

        text_x = square_center_x - text_width / 2 #added
        text_y = square_center_y - text_height / 2

        screen.blit(incorrect_surface, (x_cord * column, y_cord)) #CHANGES GO HERE
        #screen.blit(incorrect_surface, (x_cord * column, y_cord * row))
    
        #screen.blit(text, (x_cord * column, y_cord))
        screen.blit(text, (text_x, text_y)) #added

def displayKeyboard(guesses, correct):
    x_cord = SCREEN_WIDTH - 700
    y_cord = SCREEN_HEIGHT - 100
    # If there are no guesses display all letters as unguessed
    if not guesses:
        for letter in 'abcdefghijklmnopqrstuvwxyz':
            if x_cord > SCREEN_WIDTH - 80:
                x_cord = SCREEN_WIDTH - 600
                y_cord += SCREEN_HEIGHT / 20
            text = smaller_font.render(letter.upper(), False, 'black')
            screen.blit(unguessed_surface, (x_cord - 4, y_cord - 3))
            screen.blit(text, (x_cord, y_cord))
            x_cord += SCREEN_WIDTH / 20
        return
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        if x_cord > SCREEN_WIDTH - 80:
            x_cord = SCREEN_WIDTH - 600
            y_cord += SCREEN_HEIGHT / 20
        text = smaller_font.render(letter.upper(), False, 'black')
        # If the current letter is in the correct word, record the indices
        if letter in correct:
            indices = [i for i, x in enumerate(correct) if x == letter]
        else:
            indices = []
        # If the letter is in the correct word and in the correct position in any of the guesses display the green correct surface
        if letter in correct and any(guess[i] == letter for i in indices for guess in guesses):
            screen.blit(smaller_correct_surface, (x_cord - 4, y_cord - 3))
        # If the letter is in the correct word but not in the correct position in any of the guesses display the partially correct surface
        elif letter in correct and any(letter in guess for guess in guesses):
            screen.blit(smaller_partially_correct_surface, (x_cord - 4, y_cord - 3))
        # If the letter is not in the correct word display the incorrect surface
        elif any(letter in guess for guess in guesses):
            screen.blit(smaller_incorrect_surface, (x_cord - 4, y_cord - 3))
        # If the letter is not in the guess display the unguessed surface
        else:
            screen.blit(unguessed_surface, (x_cord - 4, y_cord - 3))
        screen.blit(text, (x_cord, y_cord))
        x_cord += SCREEN_WIDTH / 20

def displayEmptyBoard():
    screen.blit(logo_image, (logo_x, logo_y))
    x_cord = 120
    y_cord = 100
    for row in range(1, 7):
        for column in range(1, 6):
            screen.blit(incorrect_surface, (x_cord * column, y_cord * row)) #added -20

def draw_restart_button():
    screen.blit(restart_image, (restart_button_x, restart_button_y))

def draw_restart_button_end():
    screen.blit(restart_image, (end_restart_button_x, end_restart_button_y))

def draw_quit_button():
    screen.blit(quit_image, (quit_button_x, quit_button_y))

class Bobcat:
    x_coord = 0

    def __init__(self, s, coords):
        self.speed = s
        self.rect = bobcat_image.get_rect()
        self.rect.topleft = (Bobcat.x_coord, coords[1])
        #self.rect.topleft = coords
        Bobcat.x_coord = Bobcat.x_coord + 70
        if Bobcat.x_coord > 750:
            Bobcat.x_coord = 0

def displayBobcats(bobcats):
    for bobcat in bobcats:
        if bobcat.rect.y > 800 or bobcat.rect.y < -300:
            bobcats.remove(bobcat)

    while(len(bobcats) < 50):
        speed = random.randint(2, 4)
        coords = (random.randint(-50, 750), random.randint(-300, -100))
        new_bobcat = Bobcat(speed, coords)
        bobcats.append(new_bobcat)

    for bobcat in bobcats:
        bobcat.rect.topleft = (bobcat.rect.x, bobcat.rect.y + bobcat.speed)
        screen.blit(bobcat_image, bobcat)
    return bobcats

if __name__ == "__main__": #print game board w squares
    guesses = []
    guess = ""
    correct_word = randomword(valid_solutions)
    bobcats = []


    # Main game loop
    while True:

        #screen.fill('gray26')
        screen.fill('aquamarine4')
        bobcats = displayBobcats(bobcats)
        # This is the event loop it checks for any player input
        for event in pygame.event.get():
            # Create event for the user clicking the mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get mouse position
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Get a list of characters for each letter in the alphabet
                letters = [letter for letter in 'abcdefghijklmnopqrstuvwxyz']
                boxes = []
                x = SCREEN_WIDTH - 700
                y = SCREEN_HEIGHT - 100
                # Create a box for each letter in the alphabet and record the box coordinates in a list
                for letter in  'abcdefghijklmnopqrstuvwxyz':
                    if x > SCREEN_WIDTH - 80:
                        x = SCREEN_WIDTH - 600
                        y += SCREEN_HEIGHT / 20
                    box = pygame.Rect(x - 4, y - 3, smaller_width, smaller_height)
                    boxes.append(box)
                    x += SCREEN_WIDTH / 20
                # Check if the mouse was clicked inside any of the boxes and add it to the guess if it was
                for i in range(len(boxes)):
                    if boxes[i].collidepoint(mouse_x, mouse_y) and len(guess) < 5:
                        guess += letters[i]
                        break

                #Check if mouse clicks within bounds of restart button. If so, restart game
                if restart_button_x <= mouse_x <= restart_button_x + button_width and restart_button_y <= mouse_y <= restart_button_y + button_height:
                    guesses = []
                    guess = ""
                    correct_word = randomword(valid_solutions)
                    bobcats = []
                    continue

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
                        if guess == correct_word:
                            font_win = pygame.font.Font(None, 60)
                            text_win = font_win.render("You win!", True, (255, 255, 255))
                            text_rect = text_win.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                            screen.fill('aquamarine4')
                            screen.blit(text_win, text_rect)
                            draw_restart_button_end()
                            draw_quit_button()
                            pygame.display.update()
                            #pygame.time.delay(5000)

                            #Click functionality for restart and quit
                            guess = ""
                            while True:
                                for event in pygame.event.get():
                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        mouse_x, mouse_y = pygame.mouse.get_pos()
                                        if end_restart_button_x <= mouse_x <= end_restart_button_x + end_button_width and end_restart_button_y <= mouse_y <= end_restart_button_y + end_button_height:
                                            guesses = []
                                            guess = ""
                                            correct_word = randomword(valid_solutions)
                                            bobcats = []
                                            break
                                        elif quit_button_x <= mouse_x <= quit_button_x + quit_button_width and quit_button_y <= mouse_y <= quit_button_y + quit_button_height:
                                            pygame.quit()
                                            exit()
                                else:
                                    continue
                                break
                            
                            # pygame.quit()
                            # exit()
                        elif len(guesses) == 6 and guess != correct_word:
                            font_win = pygame.font.Font(None, 60)
                            text_win = font_win.render("You lose! Correct word: " + correct_word, True, (255, 255, 255))
                            text_rect = text_win.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                            screen.fill('aquamarine4')
                            screen.blit(text_win, text_rect)
                            draw_restart_button_end()
                            draw_quit_button()
                            pygame.display.update()
                           # pygame.time.delay(5000)

                            #Click functionality for restart and quit
                            guess = ""
                            while True:
                                for event in pygame.event.get():
                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        mouse_x, mouse_y = pygame.mouse.get_pos()
                                        if end_restart_button_x <= mouse_x <= end_restart_button_x + end_button_width and end_restart_button_y <= mouse_y <= end_restart_button_y + end_button_height:
                                            guesses = []
                                            guess = ""
                                            correct_word = randomword(valid_solutions)
                                            bobcats = []
                                            break
                                        elif quit_button_x <= mouse_x <= quit_button_x + quit_button_width and quit_button_y <= mouse_y <= quit_button_y + quit_button_height:
                                            pygame.quit()
                                            exit()
                                else:
                                    continue
                                break

                            # pygame.quit()
                            # exit()
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
        displayEmptyBoard()
        displayWords(guesses, correct_word)
        displayGuess(guess, len(guesses))
        displayKeyboard(guesses, correct_word)
        draw_restart_button()
        # Updates the display with all new objects
        pygame.display.update()

        #Sets the maximum number of iterations for the while loop per second
        clock.tick(60)