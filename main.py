import pygame, time

pygame.init()

screen = pygame.display.set_mode((500,500))
win = pygame.display.set_mode((339, 333))

font = pygame.font.SysFont("Times New Roman", 20, True)
text = font.render("AAABBBCCC", True, (255, 255, 255))
screen.fill((0, 0, 0))
screen.blit(text, (0, 0))

    #rbvtwlrbvgebvt

running = True
while running:
    #print("x")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    pygame.display.update()
        
