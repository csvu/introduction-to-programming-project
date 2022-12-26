import pygame

with open("music/music.txt",'r',encoding = 'utf-8') as v_str:
    volume_str = v_str.read()
volume = float(volume_str)
with open("music/sound.txt",'r',encoding = 'utf-8') as s_str:
    volume_sound_str = s_str.read()
volume_sound = float(volume_sound_str)

class music:
    def musicSetting(add_volume = False, minus_volume = False, add_sound = False, minus_sound = False):
        global volume
        global volume_sound
        if add_volume == True:
            volume += 0.1
            if volume >= 1.0: volume = 1.0
            volume = round(volume, 1)
            background_music.set_volume(volume)
            print(volume)
        if minus_volume == True:
            volume -= 0.1
            if volume <= 0.0: volume = 0.0
            volume = round(volume, 1)
            background_music.set_volume(volume)
            print(volume)
        if add_sound == True:
            volume_sound += 0.1
            if volume_sound >= 1.0: volume_sound = 1.0
            volume_sound = round(volume_sound, 1)
            print(volume_sound)
        if minus_sound == True:
            volume_sound -= 0.1
            if volume_sound <= 0.0: volume_sound = 0.0
            volume_sound = round(volume_sound, 1)
            print(volume_sound)
        volume_str = str(volume)
        with open("music/music.txt",'w',encoding = 'utf-8') as f: f.write(volume_str)
        volume_sound_str = str(volume_sound)
        with open("music/sound.txt",'w',encoding = 'utf-8') as f: f.write(volume_sound_str)

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
        if player_type_wrong == True and player_shooting != True:
            game_sound = pygame.mixer.Sound("music\player_type_wrong.mp3")
        if player_shooting == True:
            game_sound = pygame.mixer.Sound("music\player_shot.mp3")
        if enemy_explosion == True:
            game_sound = pygame.mixer.Sound("music\enemy_collision.mp3")
        if player_type_wrong == True and player_shooting != True:
            game_sound = pygame.mixer.Sound("music\player_type_wrong.mp3")
        game_sound.play()
        game_sound.set_volume(volume_sound)

    def displayVolumeSetting():
        global volume
        return volume

    def displaySoundSetting():
        global volume_sound
        return volume_sound