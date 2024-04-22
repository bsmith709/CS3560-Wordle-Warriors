import asyncio
import random
from sys import exit
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
pygame.mixer.init()

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

global falling_image 
bobcat_image = pygame.image.load('assets/bobcat.png')
falling_image = bobcat_image
chang = pygame.image.load('assets/CHANG.png')
among = pygame.image.load('assets/among.png')
drake = pygame.image.load('assets/drake.png')
homer = pygame.image.load('assets/Homer.png')
sonic = pygame.image.load('assets/sanic.png')
sigma = pygame.image.load('assets/sigma.png')
spike = pygame.image.load('assets/spike.png')
siege = pygame.image.load('assets/siege.png')

#Audio sounds for easter eggs
audio_among = pygame.mixer.Sound('assets/output.wav') 
audio_drake = pygame.mixer.Sound('assets/output2.wav')
audio_siege = pygame.mixer.Sound('assets/output3.wav')
audio_homer = pygame.mixer.Sound('assets/output4.wav')
audio_spike = pygame.mixer.Sound('assets/output5.wav')

restart_image = pygame.image.load('assets/restart.png')
solver_image = pygame.image.load('assets/robot_AI.png')
quit_image = pygame.image.load('assets/quit.png')

#Restart Button
button_width = 50 
button_height = 50 
restart_button_x = 740
restart_button_y = 10

solver_button_x = 740
solver_button_y = 70

# Enter button
enter_button_width = 100
enter_button_height = 50
enter_button_color = (0, 70, 0)

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
solver_image = pygame.transform.scale(solver_image, (50, 47))
quit_image = pygame.transform.scale(quit_image, (50, 47))

# Initialize the game clock to control FPS
clock = pygame.time.Clock()

#Initializes timer
start_time = pygame.time.get_ticks()
elapsed_time = 0
elapsed_time = elapsed_time // 1000 #Converts from milliseconds to seconds

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

def draw_solver_button():
    screen.blit(solver_image, (solver_button_x, solver_button_y))

def draw_restart_button_end():
    screen.blit(restart_image, (end_restart_button_x, end_restart_button_y))

def draw_quit_button():
    screen.blit(quit_image, (quit_button_x, quit_button_y))

def draw_enter_button():
    pygame.draw.rect(screen, enter_button_color, (SCREEN_WIDTH - enter_button_width - 10, SCREEN_HEIGHT - enter_button_height - 10, enter_button_width, enter_button_height))
    font = pygame.font.Font(None, 36)
    text = font.render("Enter", True, (255, 255, 255))
    text_rect = text.get_rect(center=(SCREEN_WIDTH - enter_button_width // 2 - 10, SCREEN_HEIGHT - enter_button_height // 2 - 10))
    screen.blit(text, text_rect)
class Bobcat:
    x_coord = 0

    def __init__(self, s, coords):
        self.speed = s
        self.rect = falling_image.get_rect()
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
        screen.blit(falling_image, bobcat)
    return bobcats

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

        #added
        start_time = pygame.time.get_ticks()


        # Main game loop
        while True:

            screen.fill('aquamarine4')
            bobcats = displayBobcats(bobcats)
            draw_enter_button()

            #Timer start + stop
            #added
            # elapsed_time = 0
            # elapsed_time = elapsed_time // 1000 #Converts from milliseconds to seconds  

            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - start_time) // 1000

            font = pygame.font.Font(None, 36)
            timer_text = pygame.font.Font(None, 30)
            timer_text = timer_text.render(f"Time: {elapsed_time} seconds", True, (255, 255, 255))
            screen.blit(timer_text, (10, 10))


            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - start_time
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
                        start_time = pygame.time.get_ticks() #added
                        continue





                    # Check if mouse clicks within bounds of solve button. If so, solve game
                    # if solver_button_x <= mouse_x <= solver_button_x + button_width and solver_button_y <= mouse_y <= solver_button_y + button_height:
                    #     #Implement functionality
                    #     continue
                    # If mouse clicks enter button





                    if SCREEN_WIDTH - enter_button_width - 10 <= mouse_x <= SCREEN_WIDTH - 10 and SCREEN_HEIGHT - enter_button_height - 10 <= mouse_y <= SCREEN_HEIGHT - 10:
                        if guess in valid_words:
                            new_word = True
                            guesses.append(guess)
                            frames = []
                            #Easter eggs
                            if guess == "chang":
                                falling_image = chang
                            if guess == "among":
                                falling_image = among
                                audio_among.play()
                            if guess == "drake":
                                falling_image = drake 
                                audio_drake.play()
                            if guess == "homer":
                                falling_image = homer
                                audio_homer.play()
                            if guess == "sonic":
                                falling_image = sonic
                            if guess == "sigma":
                                falling_image = sigma
                            if guess == "spike":
                                falling_image = spike
                                audio_spike.play()
                            if guess == "siege":
                                falling_image = siege
                                audio_siege.play()
                            if guess == correct_word:
                                font_win = pygame.font.Font(None, 60)
                                text_win = font_win.render("You win!", True, (255, 255, 255))
                                text_rect = text_win.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                                screen.blit(text_win, text_rect)
                                draw_restart_button_end()
                                draw_quit_button()

                                pygame.display.update()
                                while True:
                                    for event in pygame.event.get():
                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                            mouse_x, mouse_y = pygame.mouse.get_pos()
                                            if end_restart_button_x <= mouse_x <= end_restart_button_x + end_button_width and end_restart_button_y <= mouse_y <= end_restart_button_y + end_button_height:
                                                guesses = []
                                                guess = ""
                                                frames = []
                                                correct_word = randomword(valid_solutions)
                                                bobcats = []
                                                start_time = pygame.time.get_ticks() #added
                                                break
                                            elif quit_button_x <= mouse_x <= quit_button_x + quit_button_width and quit_button_y <= mouse_y <= quit_button_y + quit_button_height:
                                                pygame.quit()
                                                exit()
                                    else:
                                        continue
                                    break
                            elif len(guesses) == 6 and guess != correct_word:
                                font_win = pygame.font.Font(None, 60)
                                text_win = font_win.render("You lose! Correct word: " + correct_word, True, (255, 255, 255))
                                text_rect = text_win.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                                screen.blit(text_win, text_rect)
                                start_time = pygame.time.get_ticks() #added
                                draw_restart_button_end()
                                draw_quit_button()
                                pygame.display.update()
                                while True:
                                    for event in pygame.event.get():
                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                            mouse_x, mouse_y = pygame.mouse.get_pos()
                                            if end_restart_button_x <= mouse_x <= end_restart_button_x + end_button_width and end_restart_button_y <= mouse_y <= end_restart_button_y + end_button_height:
                                                guesses = []
                                                guess = ""
                                                falling_image = bobcat_image
                                                frames = []
                                                correct_word = randomword(valid_solutions)
                                                bobcats = []
                                                start_time = pygame.time.get_ticks() #added
                                                break
                                            elif quit_button_x <= mouse_x <= quit_button_x + quit_button_width and quit_button_y <= mouse_y <= quit_button_y + quit_button_height:
                                                pygame.quit()
                                                exit()
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
                        if guess in valid_words:
                            guesses.append(guess)
                            new_word = True
                            frames = []
                            #Easter eggs
                            if guess == "chang":
                                falling_image = chang
                            if guess == "among":
                                falling_image = among
                                audio_among.play()
                            if guess == "drake":
                                falling_image = drake
                                audio_drake.play()
                            if guess == "homer":
                                falling_image = homer
                                audio_homer.play()
                            if guess == "sonic":
                                falling_image = sonic
                            if guess == "sigma":
                                falling_image = sigma
                            if guess == "spike":
                                falling_image = spike
                                audio_spike.play()
                            if guess == "siege":
                                falling_image = siege
                                audio_siege.play()
                            if guess == correct_word:
                                font_win = pygame.font.Font(None, 60)
                                text_win = font_win.render("You win!", True, (255, 255, 255))
                                text_rect = text_win.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                                screen.fill('aquamarine4')
                                screen.blit(text_win, text_rect)
                                start_time = pygame.time.get_ticks() #added
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
                                                frames = []
                                                falling_image = bobcat_image
                                                correct_word = randomword(valid_solutions)
                                                bobcats = []
                                                start_time = pygame.time.get_ticks() #added
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
                                start_time = pygame.time.get_ticks() #added
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
                                                frames = []
                                                falling_image = bobcat_image
                                                correct_word = randomword(valid_solutions)
                                                bobcats = []
                                                start_time = pygame.time.get_ticks() #added
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
            # Updates the display with all new objects
            pygame.display.update()

            #Sets the maximum number of iterations for the while loop per second
            clock.tick(60)
            await asyncio.sleep(0)
asyncio.run(main())