import pygame, time, random

pygame.init()

screen = pygame.display.set_mode((339, 333))

font = pygame.font.SysFont("Times New Roman", 20, True)


text = font.render("AAABBBCCC", True, (111, 222, 111))
screen.fill((0, 0, 0))
x = 0
y = 0
screen.blit(text, (x, y))




running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                x += 10
                screen.fill((0, 0, 0))
                screen.blit(text, (x, y))
    pygame.display.update()

    
        