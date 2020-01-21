import pygame
import sys
from pygame.locals import *
from Bubble import Bubble
from Player import Player

pygame.init()

screen= pygame.display.set_mode((640, 460))# add a screen & screen size
screen.fill((255, 255, 255))#this change the background's color
pygame.display.set_caption('Bubble Buster!')#add caption to the display
font = pygame.font.SysFont(None, 36)

main_clock = pygame.time.Clock()
score = 0

#Adding lives
lives = 3
alive = True

#create and set up values for the player
player = Player()
player.rect.x = 250
player_speed = player.speed

draw_group = pygame.sprite.Group()
draw_group.add(player)

bubble_group = pygame.sprite.Group()

move_left = False #these are here so that the player won't be able to move at the begining of the game
move_right = False

def draw_screen():
    screen.fill((255, 255, 255))
def draw_player():
    pygame.draw.rect(screen, (47, 216, 163), player)

def draw_text(display_string, font, surface, x, y):
    text_display = font.render(display_string, 1, (178, 16, 242))
    text_rect = text_display.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_display, text_rect)

x_position = 320
y_position = 380
last_x = x_position
last_y = y_position
ball = pygame.draw.circle(screen, (242, 16, 99), (x_position, y_position), 5, 0)
ball_can_move = False

speed =[5, -5]

#values for all bubbles to use
all_bubbles = []

bubble_radius = 20
bubble_edge = 1
initial_bubble_position = 30
bubble_spacing = 60

def create_bubbles():# from here to...
    bubble_x = initial_bubble_position
    bubble_y = initial_bubble_position

    for rows in range(0, 3):
        for columns in range(0, 10):
            bubble = Bubble(bubble_x, bubble_y)
            bubble_group.add(bubble)
            bubble_x += bubble_spacing
        bubble_y += bubble_spacing
        bubble_x = initial_bubble_position

create_bubbles()

def draw_bubbles():
    for bubble in bubble_group:
        bubble = bubble_group.draw(screen)
        
            
while True:#this can be run (or exit) without crashing
    #check for events
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        #Keyboard input for players
        if event.type == KEYDOWN:
            if event.key == K_a:
                move_right = False
                move_left = True
            if event.key == K_d:
                move_left = False
                move_right = True
        if event.type == KEYUP:
            if event.key == K_a: #'K_a mean 'A key'
                move_left = False
            if event.key == K_d:
                move_right = False #just these mean we didn't update any graphic yet.
            if alive:# from here, these are game over check
                if event.key == K_SPACE:
                    ball_can_move = True
            if not alive:
                if event.key == K_RETURN:
                    lives = 3
                    alive = True
                    score = 0# from here, these are how to reset the game
                    ball_can_move = False
                    for bubble in bubble_group:
                        bubble_group.remove(bubble)
                    create_bubbles()

    #Ensure consistent frames per second
    main_clock.tick(50)
    
    #Move the player
    if move_left and player.rect.left > 0: #this means player can move no farther than from the left of the screen
            player.rect.x -= player_speed
    if move_right and player.rect.right < 640:#this means player can move no farther than from the right of the screen
            player.rect.x += player_speed

    #Move the ball
    if ball_can_move:
        last_x = x_position
        last_y = y_position

        x_position += speed[0]
        y_position += speed[1]
        if ball.x <= 0:
            x_position = 15
            speed[0] = -speed[0]
        elif ball.x >= 640:
            x_position = 625
            speed[0] = -speed[0]
        if ball.y <= 0:
            y_position = 15
            speed[1] = -speed[1] 

        #Test collisions with the player
        if ball.colliderect(player):
            y_position -= 15
            speed[1] = -speed[1]
        #Subtracting lives
        elif ball.y >= 460:
            lives -= 1
            ball_can_move = False
            
        #Move direction vector
        move_direction = ((x_position - last_x), (y_position - last_y))

        #Test collisions with the bubbles
        for bubble in bubble_group:
            if ball.colliderect(bubble.rect):
                if move_direction[1] > 0:
                    speed[1] = -speed[1]
                    y_position -= 10
                elif move_direction[1] < 0:
                    speed[1] = -speed[1]
                    y_position += 10
                bubble_group.remove(bubble)
                pygame.display.update()
                score += 100
                break
                    
    else:
        x_position = player.rect.x + 30
        
    if lives <= 0:
        alive = False
              
    draw_screen()
    draw_group.draw(screen)
    draw_bubbles()
    ball = pygame.draw.circle(screen,(242, 16, 99), (x_position, y_position), 5, 0)

    if alive:
        draw_text('Score: %s' % (score), font, screen, 5, 5)
        draw_text('Lives: %s' % (lives), font, screen, 540, 5)
    else:
        draw_text('Game Over', font, screen, 255, 5)
        draw_text('Press Enter to Play Again', font, screen, 180, 50)
    
    pygame.display.update()#this update the background



    
            
        
