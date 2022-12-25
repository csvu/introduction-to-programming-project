import pygame

volume = 1.0
volume_sound = 1.0

class music:
    def musicSetting(add_volume = False, minus_volume = False, add_sound = False, minus_sound = False):
        global volume
        global volume_sound
        if add_volume == True:
            volume += 0.1
            if volume >= 1.0: volume = 1.0
            background_music.set_volume(volume)
            print(volume)
        if minus_volume == True:
            volume -= 0.1
            if volume <= 0.0: volume = 0.0
            background_music.set_volume(volume)
            print(volume)
        if add_sound == True:
            volume_sound += 0.1
            if volume_sound >= 1.0: volume_sound = 1.0
            print(volume_sound)
        if minus_sound == True:
            volume_sound -= 0.1
            if volume_sound <= 0.0: volume_sound = 0.0
            print(volume_sound)

    def musicGame(menu_running = False, game_run = False, show_lost = False, show_win = False):
        global volume
        global background_music
        pygame.mixer.quit()
        pygame.mixer.init()
        if menu_running == True:
            background_music = pygame.mixer.Sound("music\M01.mp3")
        if game_run == True:
            background_music = pygame.mixer.Sound("music\M02.mp3")
        if show_lost == True:
            background_music = pygame.mixer.Sound("music\M04.mp3")
        if show_win == True:
            background_music = pygame.mixer.Sound("music\M05.mp3")
        background_music.play(-1) #lặp nhạc nền vô số lần
        background_music.set_volume(volume)

    def soundEffect(player_type_wrong = False, player_explosion = False, player_shooting = False, enemy_explosion = False):
        global volume_sound
        global game_sound
        pygame.mixer.init()
        if player_explosion == True:
            pygame.mixer.quit()
            pygame.mixer.init()
            game_sound = pygame.mixer.Sound("music\player_collision.mp3")
        if player_shooting == True:
            game_sound = pygame.mixer.Sound("music\player_shot.mp3")
        if enemy_explosion == True:
            game_sound = pygame.mixer.Sound("music\enemy_collision.mp3")
        if player_type_wrong == True:
            game_sound = pygame.mixer.Sound("music\player_type_wrong.mp3")
        game_sound.play()
        game_sound.set_volume(volume_sound)
