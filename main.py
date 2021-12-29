import sys

import pygame

def draw_floor():
    screen.blit(floor_surface, (floor_position, 620))
    screen.blit(floor_surface, (floor_position + 1152, 620))

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Impact', 60)

screen = pygame.display.set_mode((1152, 720))
clock = pygame.time.Clock()

## game variables
score = 0
speed = 10
floor_position = 0
duck_velocity = 0
duck_position = 420
gravity = 1.5
game_active = True

## sky
background_surface = pygame.image.load('sky.png')
background_surface = pygame.transform.scale(background_surface, (1152, 720))

## grass
floor_surface = pygame.image.load('grass_block.png')
floor_surface = pygame.transform.scale(floor_surface, (1160, 100))

## tree
tree = pygame.image.load('tree.png')
tree = pygame.transform.scale(tree, (200, 200))
tree_rect = tree.get_rect(center=(1000, 535))

## duck
duck = pygame.image.load('duck.png')
duck = pygame.transform.scale(duck, (200, 200))
duck_rect = duck.get_rect(center=(100, 520))

## game over screen
game_over = pygame.image.load('game over.jpeg')
game_over = pygame.transform.scale(game_over, (1152, 720))
space_screen = myfont.render("PRESS SPACE TO PLAY AGAIN", True, (255, 255, 255))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and duck_rect.centery == 520:
            if event.key == pygame.K_SPACE and game_active:
                duck_velocity = -35
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                score = 0
                tree_rect.centerx = 1000
                speed = 10

    ## adding surfaces
    screen.blit(background_surface, (0, 0))
    screen.blit(tree, tree_rect)
    screen.blit(duck, duck_rect)
    draw_floor()

    ##movement mechanics
    tree_rect.centerx -= speed
    floor_position -= speed

    if tree_rect.centerx <= -100:
        tree_rect.centerx = 1152
        score += 1
    if floor_position <= -1152:
        floor_position = 0

    ##score
    if score != 0 and score % 2 == 0:
        speed += .01

    ##jump mechanics
    duck_velocity += gravity
    duck_rect.centery += duck_velocity
    if duck_rect.centery >= 520:
        duck_rect.centery = 520
        duck_velocity = 0

    ##collision
    if tree_rect.centerx - duck_rect.centerx < 100 and tree_rect.centery - duck_rect.centery < 100 and tree_rect.centerx > 0:
        game_active = False
        speed = 0
        screen.blit(game_over, (0, 0))
        screen.blit(space_screen, (250, 515))

    ##score
    score_surface = myfont.render("SCORE: " + str(score), True, (255, 255, 255))
    screen.blit(score_surface, (0, 0))

    ##misc
    pygame.display.update()
    clock.tick(60)
