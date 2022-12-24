import pygame

class music:
    def musicGame(menu_running = False, game_running = False):
        pygame.mixer.quit()
        pygame.mixer.init()
        if menu_running == True:
            background_music = pygame.mixer.Sound("music\M01.mp3")
        if game_running == True:
            background_music = pygame.mixer.Sound("music\M02.mp3")
        background_music.play(-1) #lặp nhạc nền vô số lần
        background_music.set_volume(0.7)

    def soundEffect(player_explosion = False, player_shooting = False, enemy_explosion = False):
        pygame.mixer.init()
        if player_explosion == True:
            pygame.mixer.quit()
            pygame.mixer.init()
            game_sound = pygame.mixer.Sound("music\player_collision.mp3")
        if player_shooting == True:
            game_sound = pygame.mixer.Sound("music\player_shot.mp3")
        if enemy_explosion == True:
            game_sound = pygame.mixer.Sound("music\enemy_collision.mp3")
        game_sound.play()
