# import modules
import pygame
import time
import random

#initialize pygame
pygame.init()

#########################################################
# our game variables
#get colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (20, 136, 234)

display_width = 800 #game width
display_height = 600 #game height

gameDisplay = pygame.display.set_mode((display_width, display_height)) #screen size
pygame.display.set_caption('Slither') #pygame caption
icon = pygame.image.load('apple.png')
pygame.display.set_icon(icon)
img = pygame.image.load('snake.png')
appleimg = pygame.image.load('apple.png')

block_size = 20 #default size

clock = pygame.time.Clock() #get clock frames per sec

direction = 'right'

smallFont = pygame.font.SysFont('consolas', 15) #generate font variable
medFont = pygame.font.SysFont('consolas', 30) #generate font variable
largeFont = pygame.font.SysFont('consolas', 50) #generate font variable

# function for game intro menu
def game_intro():
    intro = True

    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        #The messages to screen
        gameDisplay.fill(blue)
        message_to_screen('Welcome to Slither', white, -100, 'large')
        message_to_screen('The objective of the game is to eat red apples', black, -30)
        message_to_screen('The more apples you eat, the longer you get', black, 10)
        message_to_screen('If you run into the edges you die', black, 50)
        message_to_screen('Press C to continue or Q to quit', black, 100)

        pygame.display.update()
        clock.tick(15)

#function to draw the snake
def snakeSlither(block_size, snakeList):

    if direction == 'right':
        head = pygame.transform.rotate(img, 270)
    if direction == 'left':
        head = pygame.transform.rotate(img, 90)
    if direction == 'up':
        head = img
    if direction == 'down':
        head = pygame.transform.rotate(img, 180)

    gameDisplay.blit(head, (snakeList[-1][0], snakeList[-1][1]))

    for XnY in snakeList[:-1]:
        pygame.draw.rect(gameDisplay, white, [XnY[0], XnY[1], block_size, block_size]) #draw a rectangle


def text_objects(text, color, size):

    if size == 'small':
        textSurface = smallFont.render(text, True, color)
    elif size == 'medium':
        textSurface = medFont.render(text, True, color)
    elif size == 'large':
        textSurface = largeFont.render(text, True, color)
    return textSurface, textSurface.get_rect()


#function to send message to screen
def message_to_screen(msg, color, y_displace = 0, size='small'):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (display_width / 2), (display_height / 2) + y_displace
    gameDisplay.blit(textSurf, textRect)


#function to make game loop
def gameLoop():

    global direction

    direction = 'right'

    lead_x = display_width/2 # x axis default location
    lead_y = display_height/2 # y axis default location

    lead_x_change = 20 # x axis change
    lead_y_change = 0 # y axis change

    snakeList = [] #snakeList array
    snakeLength = 1


    gameExit = False # gameExit is negative
    gameOver = False # gameOver issa negative

    randAppleX = random.randrange(0, display_width-block_size)
    randAppleY = random.randrange(0, display_height-block_size)

    #while gameExit is negative - gma should run
    while not gameExit:

        while gameOver:
            gameDisplay.fill(blue)
            message_to_screen('Game over', white, -50, size='large')
            message_to_screen('Press C to play again or Q to quit',white, 50, 'medium')
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = False
                    gameExit = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False

                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            # if the user hits quit
            if event.type == pygame.QUIT:
                gameExit = True

            # if key is pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = 'left'
                    lead_x_change -= block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    direction = 'right'
                    lead_x_change += block_size
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    direction = 'up'
                    lead_y_change -= block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    direction = 'down'
                    lead_y_change += block_size
                    lead_x_change = 0

        # if snake gets to game boundaries
        if lead_x >= display_width or lead_x <= 0 or lead_y >= display_height or lead_y <= 0:
            gameOver = True

        lead_x += lead_x_change
        lead_y += lead_y_change

        gameDisplay.fill(blue) #fill background

        AppleThickness = 30

        #pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, AppleThickness, AppleThickness])
        gameDisplay.blit(appleimg, (randAppleX, randAppleY))

        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLength:
            del snakeList[0]

        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True

        snakeSlither(block_size, snakeList) #function to draw our snake

        pygame.display.update() #update gaming surface

        # if the snake hits the apple
        if lead_x > randAppleX and lead_x < randAppleX + AppleThickness or lead_x + block_size > randAppleX and lead_x + block_size < randAppleX + AppleThickness:
            if lead_y > randAppleY and lead_y < randAppleY + AppleThickness:
                #generate random location for apple
                randAppleX = random.randrange(0, display_width-block_size)
                randAppleY = random.randrange(0, display_height-block_size)
                #increase snake size
                snakeLength += 1

            elif lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + AppleThickness:
                #generate random location for apple
                randAppleX = random.randrange(0, display_width-block_size)
                randAppleY = random.randrange(0, display_height-block_size)
                #increase snake size
                snakeLength += 1

        clock.tick(5)

    pygame.quit()
    quit()
game_intro()
gameLoop() #call game loop
