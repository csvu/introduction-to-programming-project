import pygame, time

pygame.init()

screen = pygame.display.set_mode((500,700))
win = pygame.display.set_mode((400, 700))

#RGB color values
black = (0, 0, 0)
gray = (127, 127, 127)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
cyan = (0, 255, 255)


font = pygame.font.SysFont("Times New Roman", 20, True)
text = font.render("AAABBBCCC", True, white)
screen.fill((0, 0, 0))
screen.blit(text, (0, 0))




running = True
while running:
    #print("x")git
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    pygame.display.update()
        
