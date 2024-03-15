import pygame
from sys import exit

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
example_surface = pygame.Surface((width, height))
example_surface.fill('green')

# Loading a surface from an image
filePath = 'assets/square.png'
example_surface2 = pygame.image.load(filePath)

# Creating a text surface
font_type = None
font_size = 50
example_font = pygame.font.Font(font_type, font_size)
text_surface = example_font.render('My game', False, 'black')


# Function stub to maybe be used for displaying words later
def displayWords(guesses):
    x_cord = 120
    y_cord = 100
    row = 0
    for guess in guesses:
        row += 1
        column = 0
        for letter in guess:
            column += 1
            screen.blit(example_surface, (x_cord * column, y_cord * row))
            pass

guesses = ["words", "words", "words", "words", "words", "words"]

# Main game loop
while True:

    # This is the event loop it checks for any player input
    for event in pygame.event.get():
        
        # This means the user pressed a key, this is where all of our letter inputs will be handled
        if event.type == pygame.KEYDOWN:
            # Check what key was pressed in here
            # Ex.
            if event.key == pygame.K_a: # K_a is the constant for the 'a' key, the rest of the constants are at https://www.pygame.org/docs/ref/key.html
                # blit() "A" letter image to the screen in the correct space
                pass

            # This means user hit the enter key which should mean they typed a word and need it checked
            if event.key == pygame.K_KP_ENTER: 
                # Check the word that the user is trying to use and add it to the guesses if it is valid
                pass

        # This means the user closed the window\
        if event.type == pygame.QUIT:
            # Terminates the program
            pygame.quit()
            exit()


    
    # The blit() function displays a surface at a specified coordinate
    # coords = (0,0)
    # screen.blit(example_surface2, coords)

    # Maybe use a function like this to update the display with the words?
    displayWords(guesses)

    # Updates the display with all new objects
    pygame.display.update()

    #Sets the maximum number of iterations for the while loop per second
    clock.tick(60)