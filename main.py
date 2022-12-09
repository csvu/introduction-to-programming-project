import pygame, time, random

pygame.init()

<<<<<<< HEAD
screen = pygame.display.set_mode((339, 333))

font = pygame.font.SysFont("Times New Roman", 20, True)


text = font.render("AAABBBCCC", True, (111, 222, 111))
screen.fill((0, 0, 0))
x = 0
y = 0
screen.blit(text, (x, y))
=======
width = 500
height = 750

#RGB color values
black  = (  0,   0,   0)
gray   = (127, 127, 127)
white  = (255, 255, 255)
red    = (255,   0,   0)
green  = (  0, 255,   0)
blue   = (  0,   0, 255)
yellow = (255, 255,   0)
cyan   = (  0, 255, 255)

screen = pygame.display.set_mode((width, height))

# ========== Title and Icon ==========
pygame.display.set_caption('Typing game')
icon = pygame.image.load('image/spaceship.png')
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((width, height))
win = pygame.display.set_mode((400, 700))

font = pygame.font.SysFont("Times New Roman", 20, True)
text = font.render("AAABBBCCC", True, white)
screen.fill(black)
screen.blit(text, (0, 0))
>>>>>>> 9989228bb585383d7c58ce0bdb16d5d2175e2c24


# Set Background Image When the game started
background_img = pygame.image.load("image/bg.jpg")
bg = pygame.transform.scale (background_img, (500, 750))

# ========== Player ==========
player_img = pygame.image.load('image/player_icon.png')
player_icon = pygame.transform.scale (player_img, (50, 50))
playerX = 180
playerY = 600

def player (x, y):
    screen.blit(player_icon, (x, y))

# ========== Enemy ==========
enemy_img = pygame.image.load('image/enemy_icon.png')
enemy_icon = pygame.transform.scale (enemy_img, (50, 50))
enemyX = random.randint (0, 200)
enemyY = random.randint (0, 10)
enemyX_change = 0
enemyY_change = 0

def enemy (x, y):
    screen.blit(enemy_icon, (x, y))

# ========== Bullet ===========

bullet_img = pygame.image.load('image/bullets.png')
bullet_icon = pygame.transform.scale (bullet_img, (25, 25))
bulletX = 0
bulletY = 500
bulletX_change = 0
bulletY_change = 1
bullet_state = "ready"

def bullet (x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit (bullet_icon, (x + 10, y + 100))



running = True
while running:
    #print("x")
    screen.blit(bg, (0, 0))

    #print("x")git
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
<<<<<<< HEAD
            if event.key == pygame.K_d:
                x += 10
                screen.fill((0, 0, 0))
                screen.blit(text, (x, y))
=======
                bullet (playerX, bulletY)
    

    if bullet_state is "fire":
        bullet (playerX, bulletY)
        bulletY -= bulletY_change

    if bulletY <= -150:
        bulletY = 500
        bullet_state = "ready"

    player (playerX, playerY)
    enemy (enemyX, enemyY)

>>>>>>> 9989228bb585383d7c58ce0bdb16d5d2175e2c24
    pygame.display.update()

    
        