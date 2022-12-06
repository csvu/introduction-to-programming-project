import pygame, time

pygame.init()

screen = pygame.display.set_mode((450, 750))
font = pygame.font.SysFont("Calibri", 20, True)
text = font.render("AAA", True, (255, 255, 255))
screen.fill((0, 0, 0))
screen.blit(text, (0, 0))



running = True
while running:
    #print("x")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    pygame.display.update()
        
