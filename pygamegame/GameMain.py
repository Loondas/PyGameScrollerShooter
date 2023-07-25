import pygame
import os
import random
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500

WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("First Game")

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
DAMAGE_COLORS = [WHITE, (0,255,0), YELLOW, RED, (125,125,125)]

BORDER = pygame.Rect(0,HEIGHT - 100,WIDTH,10)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Assets_grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Assets_Gun+Silencer.mp3'))

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 30
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SHIP_SPEED_X = 5
SHIP_SPEED_Y = 20

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 40, 55
COLUMN_Y_SPACE = 80
COLUMN_X_SPACE = 80

BLOCK_SIZE = (80,10)
BLOCK_PLACE = [ (i,_) for i in range(0,WIDTH,150) for _ in [HEIGHT - 100]]

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
BLOCK_HIT = pygame.USEREVENT + 3

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), 180)
RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)),0)

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('ASSETS', 'space.png')
),(WIDTH,HEIGHT))

def set_globals():
    global SHIP_SPEED_X
    global SHIP_SPEED_Y
    SHIP_SPEED_X = 5
    SHIP_SPEED_Y = 20

def initialize_enemies():
    group = []
    for y in range(4):          # Rows
        for x in range(10):     # Columns
            red = pygame.Rect((WIDTH - SPACESHIP_WIDTH)/2,100,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
            red.x, red.y = x * COLUMN_X_SPACE, y * COLUMN_Y_SPACE
            group.append(red)
    return group

def draw_enemies(group):
    group = enemy_ai(group)
    for ship in group:
        WIN.blit(RED_SPACESHIP, (ship.x, ship.y))

def enemy_ai(group):
    global SHIP_SPEED_X
    move_x = SHIP_SPEED_X
    global SHIP_SPEED_Y
    for ship in group:
        ship.x = ship.x + move_x

        if ship.x + SPACESHIP_WIDTH + SHIP_SPEED_X >= WIDTH or ship.x + SHIP_SPEED_X <= 0:
            
            SHIP_SPEED_X = -SHIP_SPEED_X
            for ship in group:    
                ship.y = ship.y + SHIP_SPEED_Y

        if ship.y + SPACESHIP_HEIGHT + SHIP_SPEED_Y >= HEIGHT - 120 or ship.y + SHIP_SPEED_Y <= -1:
            SHIP_SPEED_Y = -SHIP_SPEED_Y
            
     #       for ship in group:
     #           if ship.y + SPACESHIP_HEIGHT + SHIP_SPEED_Y >= HEIGHT - 120 or ship.y + SHIP_SPEED_Y <= -1:
      #              SHIP_SPEED_Y = -SHIP_SPEED_Y
      #              print("Switch",ship.y)
      #              ship = group[0]
      #          ship.y = ship.y + SHIP_SPEED_Y
    #        for ship in group:
     #           ship.y = ship.y + SHIP_SPEED_Y
    return group

def ai_fire(group, yellow_bullets):
    yellow = random.choice(group)
    bullet = pygame.Rect(yellow.x + yellow.width//2, yellow.y + yellow.height, 5, 10)
    yellow_bullets.append(bullet)
    BULLET_FIRE_SOUND.play()
    return yellow_bullets


    

def draw_window(red,yellow,red_bullets, yellow_bullets, red_health, yellow_health, enemies, blocks):
    WIN.blit(SPACE, (0,0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    for block in blocks:
        pygame.draw.rect(WIN, DAMAGE_COLORS[-block.health], block)
    red_health_text = HEALTH_FONT.render("Enemies Left: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, HEIGHT - 100))
    
    WIN.blit(YELLOW_SPACESHIP, (yellow.x,yellow.y))
    #WIN.blit(RED_SPACESHIP, (red.x,red.y))
    draw_enemies(enemies)


    for bullet in red_bullets:
        pygame.draw.rect(WIN,RED,bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN,YELLOW,bullet)

    pygame.display.update() 

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    set_globals()
    pygame.time.delay(5000)

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < WIDTH: # RIGHT
        yellow.x += VEL
   # if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: # UP
   #     yellow.y -= VEL
   # if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15: # Down
   #     yellow.y += VEL

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > 0: # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT -15: # DOWN
        red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, enemies, blocks):
    for bullet in yellow_bullets:
        bullet.y -= BULLET_VEL
        for block in blocks:
            if bullet.colliderect(block):
                pygame.event.post(pygame.event.Event(BLOCK_HIT))
                block.health = block.health - 1
                yellow_bullets.remove(bullet)
                if block.health == 0:
                    blocks.remove(block)
                break
        for enemy in enemies:
            if enemy.colliderect(bullet):
                pygame.event.post(pygame.event.Event(RED_HIT))
                yellow_bullets.remove(bullet)
                enemies.remove(enemy)
        if bullet.y < -10:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.y += BULLET_VEL
        for block in blocks:
            if bullet.colliderect(block):
                pygame.event.post(pygame.event.Event(BLOCK_HIT))
                block.health = block.health - 1
                red_bullets.remove(bullet) 
                if block.health == 0:
                    blocks.remove(block)
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.y > HEIGHT:
            red_bullets.remove(bullet)

def main():
    red = pygame.Rect((WIDTH - SPACESHIP_WIDTH)/2,100,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    yellow = pygame.Rect((WIDTH - SPACESHIP_WIDTH)/2,HEIGHT - 60,SPACESHIP_WIDTH,SPACESHIP_HEIGHT)
    red_bullets = []
    yellow_bullets = []
    blocks = []
    Block = type('Block', (pygame.Rect, object),{})         #Cannot set attribute to pygame.Rect, so make subclass
    for i in BLOCK_PLACE:
        
        block = Block(i[0],i[1], BLOCK_SIZE[0],BLOCK_SIZE[1])
        setattr(block, 'health', 5)
        blocks.append(block)
        
    red_health = 40
    yellow_health = 10
    enemies = initialize_enemies()

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS + ((FPS/red_health)) * 4)
        if len(red_bullets) < MAX_BULLETS and len(enemies) != 0 :
                red_bullets = ai_fire(enemies, red_bullets)
                BULLET_FIRE_SOUND.play()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width//2, yellow.y + yellow.height, 5, 10)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                    
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play() 
        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow Wins!"
        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed,red)

        handle_bullets(yellow_bullets,red_bullets,yellow,enemies,blocks)

        draw_window(red,yellow,red_bullets,yellow_bullets, red_health, yellow_health, enemies, blocks)
        
    
    main()

if __name__ == "__main__":
    main()

class Block(pygame.Rect):
    pass