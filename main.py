import asyncio
import random
from sys import exit
from queue import PriorityQueue
import pygame
import pygame.mixer

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
#pygame.mixer.init()

# Initialize the display area
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Wordle")
screen.fill('aquamarine4')

#Convert alpha and smoothscale to load with anti-aliasing
logo_image = pygame.image.load('assets/newlogo.png').convert_alpha()
logo_width = 375
logo_height = 75
logo_image = pygame.transform.smoothscale(logo_image, (logo_width, logo_height))
logo_x = (SCREEN_WIDTH - logo_image.get_width()) // 2
logo_y = 3

#Initializes falling Bobcat image
global falling_image 
bobcat_image = pygame.image.load('assets/bobcat.png')
falling_image = bobcat_image

#Loads easter eggs
chang = pygame.image.load('assets/CHANG.png')
among = pygame.image.load('assets/among.png')
drake = pygame.image.load('assets/drake.png')
homer = pygame.image.load('assets/Homer.png')
sonic = pygame.image.load('assets/sanic.png')
sigma = pygame.image.load('assets/sigma.png')
spike = pygame.image.load('assets/spike.png')
siege = pygame.image.load('assets/siege.png')

#Audio sounds for easter eggs
#audio_among = pygame.mixer.Sound('assets/output.wav') 
#audio_drake = pygame.mixer.Sound('assets/output2.wav')
#audio_siege = pygame.mixer.Sound('assets/output3.wav')
#audio_homer = pygame.mixer.Sound('assets/output4.wav')
#audio_spike = pygame.mixer.Sound('assets/output5.wav')

#Convert alpha to load with anti-aliasing
restart_image = pygame.image.load('assets/restart.png').convert_alpha()
solver_image = pygame.image.load('assets/robot_AI.png').convert_alpha()
hint_image = pygame.image.load('assets/hint.png').convert_alpha()
timer_image = pygame.image.load('assets/timer.png').convert_alpha()
backspace_image = pygame.image.load('assets/backspace.png').convert_alpha()
enter_image = pygame.image.load('assets/backspace.png').convert_alpha()

#Uniform Button Size
button_width = 50 
button_height = 50 

#Restart Button Coordinates
restart_button_x = 740
restart_button_y = 10

#Solver Button Coordinates
solver_button_x = 740
solver_button_y = 70

#Hint Button Coordinates
hint_button_x = 740
hint_button_y = 130

#Timer Button Coordinates
timer_image_x = 10
timer_image_y = 10

#Backspace Button Coordinates
backspace_button_x = 594
backspace_button_y = 685

#Enter button size + color
enter_button_width = 100
enter_button_height = 35
enter_button_color = (0, 70, 0)

#End Restart Button size + coordinates (To be removed?)
end_button_width = 200
end_button_height = 50
end_restart_button_x = (SCREEN_WIDTH - button_width) // 2
end_restart_button_y = SCREEN_HEIGHT / 2 + 50

#Image transformation using smoothscale to enable anti-aliasing
restart_image = pygame.transform.smoothscale(restart_image, (50, 47))
solver_image = pygame.transform.smoothscale(solver_image, (50, 47))
hint_image = pygame.transform.smoothscale(hint_image, (50, 47))
timer_image = pygame.transform.smoothscale(timer_image, (35, 33))
backspace_image = pygame.transform.smoothscale(backspace_image, (100, 30))
enter_image = pygame.transform.smoothscale(enter_image, (100, 30))

# Initialize the game clock to control FPS
clock = pygame.time.Clock()

#Initializes timer
start_time = pygame.time.get_ticks()
elapsed_time = 0
elapsed_time = elapsed_time // 1000 #Converts from milliseconds to seconds

# 'Surfaces' are images that can be displayed using the blit() function
width = 80
height = 80
correct_surface = pygame.image.load('assets/correctSq.png')
partially_correct_surface = pygame.image.load('assets/partialSq.png')
incorrect_surface = pygame.image.load('assets/incorrectSq.png')

# Loading a surface from an image
filePath = 'assets/square.png'
example_surface2 = pygame.image.load(filePath) #Example

# Creating a text surface
font_type = None
font_size = 75
example_font = pygame.font.Font(font_type, font_size)

# Creating smaller sizes for the keyboard
smaller_width = 30
smaller_height = 30
unguessed_surface = pygame.Surface((smaller_width, smaller_height))
unguessed_surface.fill('white')
smaller_correct_surface = pygame.image.load('assets/correctKey.png')
smaller_partially_correct_surface = pygame.image.load('assets/partialKey.png')
smaller_incorrect_surface = pygame.image.load('assets/incorrectKey.png')
smaller_font_size = 40
smaller_font = pygame.font.Font(font_type, smaller_font_size)

global frames_per_letter
frames_per_letter = 11
def animateGuess(guess, guessnum, correct, frame):
    x_coord = 120
    y_coord = 100
    row = guessnum
    column = 0

    # Math to determine where letter should be displayed
    letter_column = ((frame - (frame % frames_per_letter)) / frames_per_letter) + 1
    letter_frame = frame % frames_per_letter
    y_offset = 0
    mid_frame = ((frames_per_letter - 1) / 2)
    px_per_frame = 30 / (mid_frame + 1)
    if letter_frame <= mid_frame:
        y_offset = (letter_frame + 1) * px_per_frame
    else:
        y_offset = (frames_per_letter - letter_frame) * px_per_frame


    for letter in guess:
        column += 1

        square_center_x = x_coord * column + width / 2
        if column == letter_column:
            square_center_y = (y_coord * row + height / 2) - y_offset
        else:
            square_center_y = y_coord * row + height / 2

        text = example_font.render(letter.upper(), False, 'white')
        text_width, text_height = example_font.size(letter.upper())

        text_x = square_center_x - text_width / 2
        text_y = square_center_y - text_height / 2
        if column < letter_column:
            if letter == correct[column - 1]:
                screen.blit(correct_surface, (x_coord * column, y_coord * row))
            elif letter in correct:
                screen.blit(partially_correct_surface, (x_coord * column, y_coord * row))
            else:
                screen.blit(incorrect_surface, (x_coord * column, y_coord * row))
        else:
            screen.blit(incorrect_surface, (x_coord * column, y_coord * row))
        screen.blit(text, (text_x, text_y))

def displayWords(guesses, correct):
    x_coord = 120
    y_coord = 100
    row = 0
    for guess in guesses:
        row += 1
        column = 0
        for letter in guess:
            column += 1

            square_center_x = x_coord * column + width / 2
            square_center_y = y_coord * row + height / 2

            text = example_font.render(letter.upper(), False, 'white')
            text_width, text_height = example_font.size(letter.upper())

            text_x = square_center_x - text_width / 2
            text_y = square_center_y - text_height / 2

            if letter == correct[column - 1]:
                screen.blit(correct_surface, (x_coord * column, y_coord * row))
            elif letter in correct:
                screen.blit(partially_correct_surface, (x_coord * column, y_coord * row))
            else:
                screen.blit(incorrect_surface, (x_coord * column, y_coord * row))
            screen.blit(text, (text_x, text_y))

def displayGuess(guess, row, frames):
    x_coord = 120
    y_coord = 100 + (100 * row)
    column = 0
    for letter in guess:
        column += 1
        square_center_x = x_coord * column + width / 2
        if(frames[column - 1] < 5):
            # Offsets the guess display height based on its animation frame so it appears to slide into place
            square_center_y = (y_coord + height / 2) - (30 - (frames[column - 1] * 6))
            frames[column - 1] += 1
        else:
            square_center_y = y_coord + height / 2

        text = example_font.render(letter.upper(), False, 'white')
        text_width, text_height = example_font.size(letter.upper())

        text_x = square_center_x - text_width / 2
        text_y = square_center_y - text_height / 2

        screen.blit(incorrect_surface, (x_coord * column, y_coord))
        screen.blit(text, (text_x, text_y))

def displayKeyboard(guesses, correct):
    x_cord = SCREEN_WIDTH - 600
    y_cord = SCREEN_HEIGHT - 110
    # If there are no guesses display all letters as unguessed
    if not guesses:
        for letter in 'qwertyuiopasdfghjklzxcvbnm':
            if letter == 'a' or letter == 'z':
                if letter == 'a':
                    x_cord = SCREEN_WIDTH - 570
                if letter == 'z':
                    x_cord = SCREEN_WIDTH - 530
                y_cord += SCREEN_HEIGHT / 20
            text = smaller_font.render(letter.upper(), False, 'black')
            screen.blit(unguessed_surface, (x_cord - 4, y_cord - 3))
            screen.blit(text, (x_cord, y_cord))
            x_cord += SCREEN_WIDTH / 20
        return
    for letter in 'qwertyuiopasdfghjklzxcvbnm':
        if letter == 'a' or letter == 'z':
            if letter == 'a':
                x_cord = SCREEN_WIDTH - 570
            if letter == 'z':
                x_cord = SCREEN_WIDTH - 530
            y_cord += SCREEN_HEIGHT / 20
        text = smaller_font.render(letter.upper(), False, 'black')
        text_white = smaller_font.render(letter.upper(), False, 'white')
        # If the current letter is in the correct word, record the indices
        if letter in correct:
            indices = [i for i, x in enumerate(correct) if x == letter]
        else:
            indices = []
        # If the letter is in the correct word and in the correct position in any of the guesses display the green correct surface
        if letter in correct and any(guess[i] == letter for i in indices for guess in guesses):
            screen.blit(smaller_correct_surface, (x_cord - 4, y_cord - 3))
            screen.blit(text, (x_cord, y_cord))
        # If the letter is in the correct word but not in the correct position in any of the guesses display the partially correct surface
        elif letter in correct and any(letter in guess for guess in guesses):
            screen.blit(smaller_partially_correct_surface, (x_cord - 4, y_cord - 3))
            screen.blit(text, (x_cord, y_cord))
        # If the letter is not in the correct word display the incorrect surface
        elif any(letter in guess for guess in guesses):
            screen.blit(smaller_incorrect_surface, (x_cord - 4, y_cord - 3))
            screen.blit(text_white, (x_cord, y_cord))
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
            screen.blit(incorrect_surface, (x_cord * column, y_cord * row))

def draw_restart_button():
    screen.blit(restart_image, (restart_button_x, restart_button_y))

def draw_solver_button():
    screen.blit(solver_image, (solver_button_x, solver_button_y))

def draw_timer_button():
    screen.blit(timer_image, (timer_image_x, timer_image_y))

def draw_hint_button():
    screen.blit(hint_image, (hint_button_x, hint_button_y))

def draw_restart_button_end():
    screen.blit(restart_image, (restart_button_x, restart_button_y))#removed "end_"

def draw_enter_button():
    pygame.draw.rect(screen, enter_button_color, (SCREEN_WIDTH - enter_button_width - 155, SCREEN_HEIGHT - enter_button_height - 3, enter_button_width, enter_button_height))
    font = pygame.font.Font(None, 36)
    text = font.render("Enter", True, (255, 255, 255))
    text_rect = text.get_rect(center=(SCREEN_WIDTH - enter_button_width // 2 - 155, SCREEN_HEIGHT - enter_button_height // 2 - 3))
    screen.blit(text, text_rect)

def draw_backspace_button():
    screen.blit(backspace_image, (backspace_button_x, backspace_button_y))

class Bobcat:
    x_coord = 0

    def __init__(self, s, coords):
        self.speed = s
        self.rect = falling_image.get_rect()
        self.rect.topleft = (Bobcat.x_coord, coords[1])
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
        screen.blit(falling_image, bobcat)
    return bobcats

# Legal Check for AI solver
def ai_legal(word, guessed, unusable_letters, contains_letters, correct_letters):
    # Check if the word is in the list of guessed words
    if word in guessed:
        return False

    # Check if the word contains any of the unusable letters
    for letter in unusable_letters:
        if letter in word:
            return False

    # Check if the word contains any of the letters that the word contains
    for letter in contains_letters:
        if letter not in word:
            return False

    # Check if the word contains the correct letters in the correct positions
    for letter, position in correct_letters:
        if word[position] != letter:
            return False

    return True
# AI Solver
def ai_solve(words, guessed, unusable_letters, contains_letters, correct_letters):
    letter_freq = {}  # dictionary to store letter frequencies
    word_scores = []
    guess = "" # AI's guess

    # Loop that loads the letter frequencies dict
    for word in words:
        for letter in word:
            letter_freq[letter] = letter_freq.get(letter, 0) + 1
    # Loop that sorts the words based on letter frequencies
    for word in words:
        if ai_legal(word, guessed, unusable_letters, contains_letters, correct_letters):
            word_score = 0
            letters = set()
            for letter in word:
                if letter not in letters:
                    letters.add(letter)
            for letter in letters:
                word_score += letter_freq[letter]
            word_scores.append((word_score, word))
    word_scores.sort(reverse=True)

    return word_scores[0][1]

def notValidWordText(text_display_time):
    if(text_display_time > 0):
        font = pygame.font.Font(None, 36)
        text_not_real_word = font.render("Please only enter valid words!", True, 'white')
        screen.blit(text_not_real_word, (SCREEN_WIDTH // 2 - 170, SCREEN_HEIGHT // 2 - 328))
        text_display_time -= 1
    return text_display_time

async def main():
    global falling_image
    if __name__ == "__main__": #print game board w squares
        guesses = []
        guesses_frames = []
        frames = []
        new_word = False
        new_word_frame = 0
        
        guess = ""
        correct_word = randomword(valid_solutions)
        bobcats = []
        notValidWord = False
        text_display_time = 0

        #Starts timer
        start_time = pygame.time.get_ticks()

        # Main game loop
        while True:

            screen.fill('aquamarine4')
            bobcats = displayBobcats(bobcats)
            draw_enter_button()

            #Displays time in seconds and milliseconds. Example (7.42 seconds)
            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - start_time) / 1000.0
            seconds = int(elapsed_time)
            milliseconds = int((elapsed_time - seconds) * 100)
            elapsed_time_str = f"{seconds}.{milliseconds}"

            font = pygame.font.Font(None, 36)
            timer_text = pygame.font.Font(None, 30)
            draw_timer_button()
            timer_text = timer_text.render(f"{elapsed_time_str}", True, (255, 255, 255))
            screen.blit(timer_text, (48, 17))

            # This is the event loop it checks for any player input
            for event in pygame.event.get():
                # Create event for the user clicking the mouse
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Get mouse position
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    # Get a list of characters for each letter in the alphabet
                    letters = [letter for letter in 'qwertyuiopasdfghjklzxcvbnm']
                    boxes = []
                    x = SCREEN_WIDTH - 600
                    y = SCREEN_HEIGHT - 110
                    # Create a box for each letter in the alphabet and record the box coordinates in a list
                    for letter in  'qwertyuiopasdfghjklzxcvbnm':
                        if letter == 'a' or letter == 'z':
                            if letter == 'a':
                                x = SCREEN_WIDTH - 570
                            if letter == 'z':
                                x = SCREEN_WIDTH - 530
                            y += SCREEN_HEIGHT / 20
                        box = pygame.Rect(x - 4, y - 3, smaller_width, smaller_height)
                        boxes.append(box)
                        x += SCREEN_WIDTH / 20
                    # Check if the mouse was clicked inside any of the boxes and add it to the guess if it was
                    for i in range(len(boxes)):
                        if boxes[i].collidepoint(mouse_x, mouse_y) and len(guess) < 5:
                            guess += letters[i]
                            frames.append(0)
                            break

                    # Check if mouse clicks within bounds of restart button. If so, restart game
                    if restart_button_x <= mouse_x <= restart_button_x + button_width and restart_button_y <= mouse_y <= restart_button_y + button_height:
                        guesses = []
                        guess = ""
                        frames = []
                        falling_image = bobcat_image
                        correct_word = randomword(valid_solutions)
                        bobcats = []
                        new_word = False
                        start_time = pygame.time.get_ticks() #added
                        continue

                    #PLACEHOLDERS
                    # Check if mouse clicks within bounds of solve button. If so, solve game
                    if solver_button_x <= mouse_x <= solver_button_x + button_width and solver_button_y <= mouse_y <= solver_button_y + button_height:
                        unusable_letters = []
                        contains_letters = []
                        correct_letters = []
                        for guess in guesses:
                            for letter in guess:
                                if letter not in correct_word:
                                    unusable_letters.append(letter)
                                elif guess.index(letter) == correct_word.index(letter):
                                    correct_letters.append((letter, guess.index(letter)))
                                else:
                                    contains_letters.append(letter)
                        guess = ai_solve(valid_words, guesses, unusable_letters, contains_letters, correct_letters)
                        for letter in guess:
                            frames.append(0)
                        continue

                    #Same for hint
                    if hint_button_x <= mouse_x <= hint_button_x + button_width and hint_button_y <= mouse_y <= hint_button_y + button_height:
                        unusable_letters = []
                        contains_letters = []
                        correct_letters = []
                        for guess in guesses:
                            for letter in guess:
                                if letter not in correct_word:
                                    unusable_letters.append(letter)
                                elif guess.index(letter) == correct_word.index(letter):
                                    correct_letters.append((letter, guess.index(letter)))
                                else:
                                    contains_letters.append(letter)
                        guess = ai_solve(valid_words, guesses, unusable_letters, contains_letters, correct_letters)
                        continue

                    # Check if mouse clicks within bounds of backspace button. If so, remove last letter from guess
                    if backspace_button_x <= mouse_x <= backspace_button_x + button_width and backspace_button_y <= mouse_y <= backspace_button_y + button_height:
                        if len(guess) > 0:
                            guess = guess[0:-1]
                            frames = frames[0:-1]

                    if SCREEN_WIDTH - enter_button_width - 155 <= mouse_x <= SCREEN_WIDTH - 155 and SCREEN_HEIGHT - enter_button_height - 3 <= mouse_y <= SCREEN_HEIGHT - 3:
                        if guess in valid_words and guess not in guesses:
                            new_word = True
                            guesses.append(guess)
                            frames = []
                            #Easter eggs
                            if guess == "chang":
                                falling_image = chang
                            if guess == "among":
                                falling_image = among
                                #audio_among.play()
                            if guess == "drake":
                                falling_image = drake 
                                #audio_drake.play()
                            if guess == "homer":
                                falling_image = homer
                                #audio_homer.play()
                            if guess == "sonic":
                                falling_image = sonic
                            if guess == "sigma":
                                falling_image = sigma
                            if guess == "spike":
                                falling_image = spike
                                #audio_spike.play()
                            if guess == "siege":
                                falling_image = siege
                                #audio_siege.play()
                            if guess == correct_word:
                                # font_win = pygame.font.Font(None, 60)
                                # text_win = font_win.render("You win!", True, (255, 255, 255))
                                # text_rect = text_win.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                                # screen.blit(text_win, text_rect)
                                # draw_restart_button_end()

                                # New function to show elapsed time on three separate lines.
                                # Implemented to use with win/loss removed
                                screen.fill('aquamarine4')
                                displayKeyboard(guesses, correct_word)
                                displayWords(guesses, correct_word)
                                font_win = pygame.font.Font(None, 30)
                                font_win2 = pygame.font.Font(None, 30)
                                font_win3 = pygame.font.Font(None, 30)
                                text_win = font_win.render("You win!", True, (255, 255, 255))
                                # text_win2 = font_win2.render(f"Time Taken: {elapsed_time // 1000} seconds.", True, (255, 255, 255))
                                text_win2 = font_win2.render(f"Time Taken: {elapsed_time_str} seconds", True, (255, 255, 255))
                                text_win3 = font_win3.render("Correct Word: " + correct_word, True, (255, 255, 255))
                                text_rect = text_win.get_rect(center=(SCREEN_WIDTH // 2, 25)) #removed screen_height // 2 - 40
                                text_rect2 = text_win2.get_rect(center=(SCREEN_WIDTH // 2, 50)) #removed screen height // 2 + 20
                                text_rect3 = text_win3.get_rect(center=(SCREEN_WIDTH // 2, 75))
                                overlay_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                                overlay_surface.fill((0, 0, 0, 128))  # Transparent black overlay
                                screen.blit(overlay_surface, (0, 0))
                                screen.blit(text_win, text_rect)
                                screen.blit(text_win2, text_rect2)
                                screen.blit(text_win3, text_rect3)
                                start_time = pygame.time.get_ticks()
                                draw_restart_button_end()
                                pygame.display.update()

                                pygame.display.update()
                                while True:
                                    for event in pygame.event.get():
                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                            mouse_x, mouse_y = pygame.mouse.get_pos()
                                            #changed end_restart_button_x to restart_button coordinates. added
                                            if restart_button_x <= mouse_x <= restart_button_x + end_button_width and restart_button_y <= mouse_y <= restart_button_y + button_height:
                                                guesses = []
                                                guess = ""
                                                frames = []
                                                falling_image = bobcat_image
                                                correct_word = randomword(valid_solutions)
                                                bobcats = []
                                                new_word = False
                                                start_time = pygame.time.get_ticks()
                                                break
                                    else:
                                        continue
                                    break
                            elif len(guesses) == 6 and guess != correct_word:
                                # font_win = pygame.font.Font(None, 60)
                                # text_win = font_win.render("You lose! Correct word: " + correct_word, True, (255, 255, 255))
                                # text_rect = text_win.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                                # screen.fill('aquamarine4')
                                # screen.blit(text_win, text_rect)
                                # start_time = pygame.time.get_ticks()
                                # draw_restart_button_end()
                                # pygame.display.update()

                                # #New function to show elapsed time on two separate lines.
                                # #Implemented to use with win/loss removed
                                # font_win = pygame.font.Font(None, 60)
                                # font_win2 = pygame.font.Font(None, 60)
                                # text_win = font_win.render(f"You lost in {elapsed_time // 1000} seconds.", True, (255, 255, 255))
                                # text_win2 = font_win2.render("Correct word: " + correct_word, True, (255, 255, 255))
                                # text_rect = text_win.get_rect(center=(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) - 40))
                                # text_rect2 = text_win2.get_rect(center=(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) + 20))
                                # screen.blit(text_win, text_rect)
                                # screen.blit(text_win2, text_rect2)
                                # start_time = pygame.time.get_ticks()
                                # draw_restart_button_end()
                                # pygame.display.update()

                                # New function to show elapsed time on three separate lines.
                                # Implemented to use with win/loss removed
                                screen.fill('aquamarine4')
                                displayKeyboard(guesses, correct_word)
                                displayWords(guesses, correct_word)
                                font_win = pygame.font.Font(None, 30)
                                font_win2 = pygame.font.Font(None, 30)
                                font_win3 = pygame.font.Font(None, 30)
                                text_win = font_win.render("You lost.", True, (255, 255, 255))
                                # text_win2 = font_win2.render(f"Time Taken: {elapsed_time // 1000} seconds.", True, (255, 255, 255))
                                text_win2 = font_win2.render(f"Time Taken: {elapsed_time_str} seconds", True, (255, 255, 255))
                                text_win3 = font_win3.render("Correct Word: " + correct_word, True, (255, 255, 255))
                                text_rect = text_win.get_rect(center=(SCREEN_WIDTH // 2, 25)) #removed screen_height // 2 - 40
                                text_rect2 = text_win2.get_rect(center=(SCREEN_WIDTH // 2, 50)) #removed screen height // 2 + 20
                                text_rect3 = text_win3.get_rect(center=(SCREEN_WIDTH // 2, 75))
                                overlay_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                                overlay_surface.fill((0, 0, 0, 128))  # Transparent black overlay
                                screen.blit(overlay_surface, (0, 0))
                                screen.blit(text_win, text_rect)
                                screen.blit(text_win2, text_rect2)
                                screen.blit(text_win3, text_rect3)
                                start_time = pygame.time.get_ticks()
                                draw_restart_button_end()
                                pygame.display.update()

                                while True:
                                    for event in pygame.event.get():
                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                            mouse_x, mouse_y = pygame.mouse.get_pos()
                                            #changed end_restart_button_x to restart_button coordinates. added
                                            if restart_button_x <= mouse_x <= restart_button_x + end_button_width and restart_button_y <= mouse_y <= restart_button_y + end_button_height:
                                                guesses = []
                                                guess = ""
                                                frames = []
                                                falling_image = bobcat_image
                                                correct_word = randomword(valid_solutions)
                                                bobcats = []
                                                new_word = False
                                                start_time = pygame.time.get_ticks()
                                                break
                                    else:
                                        continue
                                    break
                            guess = ""

                # This means the user pressed a key, this is where all of our letter inputs are handled
                if event.type == pygame.KEYDOWN:

                    if len(guess) < 5:
                        if event.key == pygame.K_a: # K_a is the constant for the 'a' key, the rest of the constants are at https://www.pygame.org/docs/ref/key.html
                            guess += "a"
                            frames.append(0)
                        elif event.key == pygame.K_b:
                            guess += "b"
                            frames.append(0) 
                        elif event.key == pygame.K_c:
                            guess += "c"
                            frames.append(0)
                        elif event.key == pygame.K_d:
                            guess += "d"
                            frames.append(0)
                        elif event.key == pygame.K_e:
                            guess += "e"
                            frames.append(0)
                        elif event.key == pygame.K_f:
                            guess += "f"
                            frames.append(0)
                        elif event.key == pygame.K_g:
                            guess += "g"
                            frames.append(0)
                        elif event.key == pygame.K_h:
                            guess += "h"
                            frames.append(0)
                        elif event.key == pygame.K_i:
                            guess += "i"
                            frames.append(0)
                        elif event.key == pygame.K_j:
                            guess += "j"
                            frames.append(0)
                        elif event.key == pygame.K_k:
                            guess += "k"
                            frames.append(0)
                        elif event.key == pygame.K_l:
                            guess += "l"
                            frames.append(0)
                        elif event.key == pygame.K_m:
                            guess += "m"
                            frames.append(0)
                        elif event.key == pygame.K_n:
                            guess += "n"
                            frames.append(0)
                        elif event.key == pygame.K_o:
                            guess += "o"
                            frames.append(0)
                        elif event.key == pygame.K_p:
                            guess += "p"
                            frames.append(0)
                        elif event.key == pygame.K_q:
                            guess += "q"
                            frames.append(0)
                        elif event.key == pygame.K_r:
                            guess += "r"
                            frames.append(0)
                        elif event.key == pygame.K_s: 
                            guess += "s"
                            frames.append(0)
                        elif event.key == pygame.K_t: 
                            guess += "t"
                            frames.append(0)
                        elif event.key == pygame.K_u: 
                            guess += "u"
                            frames.append(0)
                        elif event.key == pygame.K_v: 
                            guess += "v"
                            frames.append(0)
                        elif event.key == pygame.K_w: 
                            guess += "w"
                            frames.append(0)
                        elif event.key == pygame.K_x: 
                            guess += "x"
                            frames.append(0)
                        elif event.key == pygame.K_y: 
                            guess += "y"
                            frames.append(0)
                        elif event.key == pygame.K_z: 
                            guess += "z"
                            frames.append(0)

                    if event.key == pygame.K_BACKSPACE: 
                        guess = guess[0:-1]
                        frames = frames[0:-1]

                    # This means user hit the enter key which should mean they typed a word and need it checked
                    if event.key == pygame.K_RETURN: 
                        if guess in valid_words and guess not in guesses:
                            guesses.append(guess)
                            new_word = True
                            frames = []
                            #Easter eggs
                            if guess == "chang":
                                falling_image = chang
                            if guess == "among":
                                falling_image = among
                                #audio_among.play()
                            if guess == "drake":
                                falling_image = drake
                                #audio_drake.play()
                            if guess == "homer":
                                falling_image = homer
                                #audio_homer.play()
                            if guess == "sonic":
                                falling_image = sonic
                            if guess == "sigma":
                                falling_image = sigma
                            if guess == "spike":
                                falling_image = spike
                                #audio_spike.play()
                            if guess == "siege":
                                falling_image = siege
                                #audio_siege.play()
                            if guess == correct_word:
                                # screen.fill('aquamarine4')
                                # displayKeyboard(guesses, correct_word)
                                # displayWords(guesses, correct_word)
                                # font_win = pygame.font.Font(None, 60)
                                # text_win = font_win.render("You win! Correct word: " + correct_word, True, (255, 255, 255))
                                # text_rect = text_win.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                                # overlay_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                                # overlay_surface.fill((0, 0, 0, 128))  # Transparent black overlay
                                # screen.blit(overlay_surface, (0, 0))
                                # screen.blit(text_win, text_rect)
                                # start_time = pygame.time.get_ticks() #added
                                # draw_restart_button_end()
                                # pygame.display.update()
                                # New function to show elapsed time on three separate lines.
                                # Implemented to use with win/loss removed
                                screen.fill('aquamarine4')
                                displayKeyboard(guesses, correct_word)
                                displayWords(guesses, correct_word)
                                font_win = pygame.font.Font(None, 30)
                                font_win2 = pygame.font.Font(None, 30)
                                font_win3 = pygame.font.Font(None, 30)
                                text_win = font_win.render("You win!", True, (255, 255, 255))
                                # text_win2 = font_win2.render(f"Time Taken: {elapsed_time // 1000} seconds.", True, (255, 255, 255))
                                text_win2 = font_win2.render(f"Time Taken: {elapsed_time_str} seconds", True, (255, 255, 255))
                                text_win3 = font_win3.render("Correct Word: " + correct_word, True, (255, 255, 255))
                                text_rect = text_win.get_rect(center=(SCREEN_WIDTH // 2, 25)) #removed screen_height // 2 - 40
                                text_rect2 = text_win2.get_rect(center=(SCREEN_WIDTH // 2, 50)) #removed screen height // 2 + 20
                                text_rect3 = text_win3.get_rect(center=(SCREEN_WIDTH // 2, 75))
                                overlay_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                                overlay_surface.fill((0, 0, 0, 128))  # Transparent black overlay
                                screen.blit(overlay_surface, (0, 0))
                                screen.blit(text_win, text_rect)
                                screen.blit(text_win2, text_rect2)
                                screen.blit(text_win3, text_rect3)
                                start_time = pygame.time.get_ticks()
                                draw_restart_button_end()
                                pygame.display.update()

                                #Click functionality for restart and quit
                                guess = ""
                                while True:
                                    for event in pygame.event.get():
                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                            mouse_x, mouse_y = pygame.mouse.get_pos()
                                            #changed end_restart_button_x to restart_button coordinates. added
                                            if restart_button_x <= mouse_x <= restart_button_x + end_button_width and restart_button_y <= mouse_y <= restart_button_y + end_button_height:
                                                guesses = []
                                                guess = ""
                                                frames = []
                                                falling_image = bobcat_image
                                                correct_word = randomword(valid_solutions)
                                                bobcats = []
                                                new_word = False
                                                start_time = pygame.time.get_ticks()
                                                break
                                    else:
                                        continue
                                    break
                                
                                # pygame.quit()
                                # exit()
                            elif len(guesses) == 6 and guess != correct_word:
                                # screen.fill('aquamarine4')
                                # displayKeyboard(guesses, correct_word)
                                # displayWords(guesses, correct_word)
                                # font_win = pygame.font.Font(None, 60)
                                # text_win = font_win.render("You lose! Correct word: " + correct_word, True, (255, 255, 255))
                                # text_rect = text_win.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                                # overlay_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                                # overlay_surface.fill((0, 0, 0, 128))  # Transparent black overlay
                                # screen.blit(overlay_surface, (0, 0))
                                # screen.blit(text_win, text_rect)
                                # start_time = pygame.time.get_ticks() #added
                                # draw_restart_button_end()
                                # pygame.display.update()

                                # New function to show elapsed time on two separate lines.
                                # Implemented to use with win/loss removed
                                screen.fill('aquamarine4')
                                displayKeyboard(guesses, correct_word)
                                displayWords(guesses, correct_word)
                                # font_win = pygame.font.Font(None, 60)
                                # font_win2 = pygame.font.Font(None, 60)
                                # text_win = font_win.render(f"You lost in {elapsed_time // 1000} seconds.", True, (255, 255, 255))
                                # text_win2 = font_win2.render("Correct word: " + correct_word, True, (255, 255, 255))
                                # text_rect = text_win.get_rect(center=(SCREEN_WIDTH // 2, 25)) #removed screen_height // 2 - 40
                                # text_rect2 = text_win2.get_rect(center=(SCREEN_WIDTH // 2, 70)) #removed screen height // 2 + 20
                                font_win = pygame.font.Font(None, 30)
                                font_win2 = pygame.font.Font(None, 30)
                                font_win3 = pygame.font.Font(None, 30)
                                text_win = font_win.render("You lost.", True, (255, 255, 255))
                                # text_win2 = font_win2.render(f"Time Taken: {elapsed_time // 1000} seconds.", True, (255, 255, 255))
                                text_win2 = font_win2.render(f"Time Taken: {elapsed_time_str} seconds", True, (255, 255, 255))
                                text_win3 = font_win3.render("Correct Word: " + correct_word, True, (255, 255, 255))
                                text_rect = text_win.get_rect(center=(SCREEN_WIDTH // 2, 25)) #removed screen_height // 2 - 40
                                text_rect2 = text_win2.get_rect(center=(SCREEN_WIDTH // 2, 50)) #removed screen height // 2 + 20
                                text_rect3 = text_win3.get_rect(center=(SCREEN_WIDTH // 2, 75))
                                overlay_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                                overlay_surface.fill((0, 0, 0, 128))  # Transparent black overlay
                                screen.blit(overlay_surface, (0, 0))
                                screen.blit(text_win, text_rect)
                                screen.blit(text_win2, text_rect2)
                                screen.blit(text_win3, text_rect3)
                                start_time = pygame.time.get_ticks()
                                draw_restart_button_end()
                                pygame.display.update()



                                #Click functionality for restart and quit
                                guess = ""
                                while True:
                                    for event in pygame.event.get():
                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                            mouse_x, mouse_y = pygame.mouse.get_pos()
                                            #changed end_restart_button_x to restart_button coordinates. added
                                            if restart_button_x <= mouse_x <= restart_button_x + end_button_width and restart_button_y <= mouse_y <= restart_button_y + end_button_height:
                                                guesses = []
                                                guess = ""
                                                frames = []
                                                falling_image = bobcat_image
                                                correct_word = randomword(valid_solutions)
                                                bobcats = []
                                                new_word = False
                                                start_time = pygame.time.get_ticks()
                                                break
                                    else:
                                        continue
                                    break

                                # pygame.quit()
                                # exit()
                            guess = ""
                        elif guess not in valid_words and len(guess) == 5:
                            notValidWord = True
                            text_display_time = 120
                        pass

                # This means the user closed the window
                if event.type == pygame.QUIT:
                    # Terminates the program
                    pygame.quit()
                    exit()

            # Display guesses and current word being typed
            displayEmptyBoard()
            if new_word:
                if len(guesses) > 1:
                    displayWords(guesses[0:-1], correct_word)
                    animateGuess(guesses[-1], len(guesses), correct_word, new_word_frame)
                else:
                    animateGuess(guesses[-1], len(guesses), correct_word, new_word_frame)
                new_word_frame += 1
                if new_word_frame > (frames_per_letter * 5) - 1:
                    new_word = False
                    new_word_frame = 0
            else:
                displayWords(guesses, correct_word)
            displayGuess(guess, len(guesses), frames)
            displayKeyboard(guesses, correct_word)
            draw_restart_button()
            draw_solver_button()
            draw_hint_button()
            draw_backspace_button()
            if notValidWord:
                text_display_time = notValidWordText(text_display_time)
                if text_display_time == 0:
                    notValidWord = False
            # Updates the display with all new objects
            pygame.display.update()

            #Sets the maximum number of iterations for the while loop per second
            clock.tick(60)
            await asyncio.sleep(0)
asyncio.run(main())