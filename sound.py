import pygame

class music:
    def musicGame(menu_running, game_running):
        pygame.mixer.init()
        if menu_running == True:
            pygame.mixer.music.load("music\M01.mp3")
            pygame.mixer.music.play(-1) #lặp nhạc nền vô số lần
        if game_running == True:
            pygame.mixer.music.load("music\M02.mp3")
            pygame.mixer.music.play(-1)

    def soundEffect():
        pygame.mixer.quit()
        pygame.init()
        pygame.mixer.init()
        if True:
            pygame.mixer.music.load("music\player_collision.mp3")
            pygame.mixer.music.play()
