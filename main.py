from pygame import mouse
import pygame.font
import pygame.display
import pygame.image
import pygame.draw
import pygame.event
import pygame.rect
import pygame.time
import pygame.image
from pygame.constants import QUIT
from time import sleep
from random import randint
import pygame


def initBody(x, y):
    l = []
    for i in range(10, 100, 10):
        l.append([x - i, y])
    return l

def bodyCollision(x, y, posBody):
    for pos in posBody:
        if x == pos[0] and y == pos[1]:
            return False
    return True

def headCollision(x, y):
    return (x < 990 and x > 0 and y < 790 and y > 0)

def animation(screen, gameOver, retry, stop, font):
    for i in range(1, 253):
        sleep(0.004)
        screen.fill((0,0,0))
        screen.blit(gameOver, pygame.Rect(300, 275, 10,10))
        gameOver.set_alpha(i + 2)
        retry.set_alpha(i + 2)
        stop.set_alpha(i + 2)
        screen.blit(retry, (300, 550))
        screen.blit(stop, (300 + gameOver.get_width() - stop.get_width(), 550))
        pygame.display.update()

    # Waiting for input of player
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry.get_rect(x=300, y= 550).collidepoint(pygame.mouse.get_pos()):
                    return True
                if stop.get_rect(x=300 + gameOver.get_width() - stop.get_width(), y= 550).collidepoint(pygame.mouse.get_pos()):
                    return False

        #Hover effect for buttons
        if retry.get_rect(x=300, y= 550).collidepoint(pygame.mouse.get_pos()):
            retry = font.render("Retry", True, (255,255,255))
            screen.blit(retry, (300, 550))
            pygame.display.update()
        elif stop.get_rect(x=300 + gameOver.get_width() - stop.get_width(), y= 550).collidepoint(pygame.mouse.get_pos()):
            stop = font.render("Quit", True, (255,255,255))
            screen.blit(stop, (300 + gameOver.get_width() - stop.get_width(), 550))
            pygame.display.update()
        else:
            retry = font.render("Retry", True, (50, 50,50))
            stop = font.render("Quit", True, (50, 50,50))
            screen.blit(retry, (300, 550))
            screen.blit(stop, (300 + gameOver.get_width() - stop.get_width(), 550))
            pygame.display.update()
def main():
    pygame.init()
    RECTSIZE = 10
    GREYBORDER = pygame.Color(50, 50, 50)
    RED = pygame.Color(255, 0, 0)
    GREEN = pygame.Color(0, 255, 0)
    BLUE = pygame.Color(0, 0, 255)
    count = 0
    x = 100
    y = 50
    score = 0
    directionX = 10
    directionY = 0
    fps = pygame.time.Clock()
    posBody = initBody(x, y)
    apples = [[randint(1, 98) * 10, randint(1, 78) * 10]]
    running = True
    starting = True
    screen = pygame.display.set_mode((1000,800))
    pygame.display.set_caption("Snake")
    pygame.display.set_icon(pygame.image.load("Assets/Snake_icon.png"))
    gameOver = pygame.transform.scale(pygame.image.load("Assets/game-over.png"), (400, 250))
    start = pygame.transform.scale(pygame.image.load("Assets/Snake_start.png"), (250, 230))
    font = pygame.font.Font("Assets/LoveGlitch.ttf", 80)
    playButton = font.render("Play", True, GREYBORDER)
    retry = font.render("Retry", True, GREYBORDER)
    stop = font.render("Quit", True, GREYBORDER)

    # Starting screen
    screen.blit(start, (375, 200))
    screen.blit(playButton, (442, 450))
    for i in range(0, 800, 10):
            pygame.draw.rect(screen , GREYBORDER, pygame.Rect(990, i, RECTSIZE, RECTSIZE))
            pygame.draw.rect(screen , GREYBORDER, pygame.Rect(0, i, RECTSIZE, RECTSIZE))
    for j in range(10, 1000, 10):
        pygame.draw.rect(screen , GREYBORDER, pygame.Rect(j,0, RECTSIZE, RECTSIZE))
        pygame.draw.rect(screen , GREYBORDER, pygame.Rect(j,790, RECTSIZE, RECTSIZE))
    pygame.display.update()

    while starting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                starting = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    starting = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # TODO Simplify code with animation function
                if playButton.get_rect(x=442, y= 450).collidepoint(pygame.mouse.get_pos()):
                    playButton = font.render("Play", True, (255,255,255))
                    screen.blit(playButton, (442, 450))
                    pygame.display.update()
                    sleep(0.08)
                    starting = False

        if playButton.get_rect(x=442, y= 450).collidepoint(pygame.mouse.get_pos()):
                    playButton = font.render("Play", True, (255,255,255))
                    screen.blit(playButton, (442, 450))
                    pygame.display.update()
        else:
            playButton = font.render("Play", True, GREYBORDER)
            screen.blit(playButton, (442, 450))
            pygame.display.update()

    # game Loop
    while running:
        # ========== Managing time ===============
        fps.tick(int(score/2) + 4)
        count += 1
        if count % 16 == 0:
            apples.append([randint(1, 98) * 10, randint(1, 78) * 10])
        # ========== Handling events ==============
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and directionX == 0:
                    directionX = 10
                    directionY = 0
                    break
                elif event.key == pygame.K_LEFT and directionX == 0:
                    directionX = -10
                    directionY = 0
                    break
                elif event.key == pygame.K_UP and directionY == 0:
                    directionY = -10
                    directionX = 0
                    break
                elif event.key == pygame.K_DOWN and directionY == 0:
                    directionY = 10
                    directionX = 0
                    break

        # ======= Updating parameters - Game logic ==============
        temp = [x, y]
        temp2 = [0, 0]

        # Collision detection
        if headCollision(x+ directionX, y + directionY) and bodyCollision(x + directionX, y + directionY,posBody):
            x += directionX
            y += directionY
        else:
            running = animation(screen, gameOver, retry, stop, font)
            if running:
                x = 100
                y = 50
                directionX = 10
                directionY = 0
                count = 0
                temp = [x, y]
                posBody.clear()
                posBody = initBody(x, y)
                print(posBody)
                apples = [[randint(1, 98) * 10, randint(1, 78) * 10]]
            else:
                break
            
        
        # Checking apples positions
        for apple in apples:
            if x == apple[0] and y == apple[1]:
                posBody.append([posBody[len(posBody) - 1][0] - abs(directionX), posBody[len(posBody) - 1][1] - abs(directionY)])
                apples.remove(apple)
                score += 1
        
        # Updating body position
        for position in posBody:
            temp2[0] = position[0]
            temp2[1] = position[1]
            position[0] = temp[0]
            position[1] = temp[1]
            temp[0] = temp2[0]
            temp[1] = temp2[1]
        
        # ========== Drawing the map ==========
        screen.fill((0,0,0))
        for i in range(0, 800, 10):
            pygame.draw.rect(screen , GREYBORDER, pygame.Rect(990, i, RECTSIZE, RECTSIZE))
            pygame.draw.rect(screen , GREYBORDER, pygame.Rect(0, i, RECTSIZE, RECTSIZE))
        for j in range(10, 1000, 10):
            pygame.draw.rect(screen , GREYBORDER, pygame.Rect(j,0, RECTSIZE, RECTSIZE))
            pygame.draw.rect(screen , GREYBORDER, pygame.Rect(j,790, RECTSIZE, RECTSIZE))

        # ========== Drawing the apples =========
        for apple in apples:
            pygame.draw.rect(screen, RED, pygame.Rect(apple[0], apple[1], RECTSIZE, RECTSIZE))
        # =========== Drawing the snake ========

        pygame.draw.rect(screen, BLUE, pygame.Rect(x, y, RECTSIZE, RECTSIZE))
        for l in posBody:
            pygame.draw.rect(screen, GREEN, pygame.Rect(l[0], l[1], RECTSIZE, RECTSIZE))
        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()