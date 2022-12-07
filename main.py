import pygame, time

pygame.init()

<<<<<<< HEAD
screen = pygame.display.set_mode((450,450))
=======
screen = pygame.display.set_mode((450, cd50))
>>>>>>> 94e6fe54de18ad0247b75625efec6722d9671e84
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
        
