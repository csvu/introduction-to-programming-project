import pygame, math, os, time, random
from sound import music #từ sound.py móc class music ra


pygame.init()

WIDTH, HEIGHT = 430, 650
modern_grey = (42, 42, 42)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A mishmash")

small_enemy = pygame.image.load(os.path.realpath("image/small_enemy2.png"))
player_icon = pygame.image.load(os.path.realpath("image/player_icon2.png"))
enery_circle = pygame.image.load(os.path.relpath("image/energy_circle2.png"))
hidden_thing = pygame.image.load(os.path.realpath("image/hidden_thing.png"))
background = pygame.image.load(os.path.realpath("image/background.png"))



font = pygame.font.SysFont("Calibri", 20, True)

def isObjsCollision(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

class Bullet:
    def __init__(self, x, y, image, enemy):
        self.x = x
        self.y = y
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.chosen_enemy = enemy

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def move(self, speed):
        unit_x, unit_y = self.chosen_enemy.x - self.x, self.chosen_enemy.y - self.y
        dist = math.hypot(unit_x, unit_y)
        unit_x, unit_y = unit_x / dist, unit_y / dist
        self.x += unit_x * speed
        self.y += unit_y * speed

    def isOutOfScreen(self):
        return not(self.y <= HEIGHT and self.y >= 0)

    def isBulletCollision(self, obj):
        return isObjsCollision(self, obj)


class Shuttle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shuttle_image = None

    def draw(self):
        screen.blit(self.shuttle_image, (self.x, self.y))

    def getWidth(self):
        return self.shuttle_image.get_width()

    def getHeight(self):
        return self.shuttle_image.get_height()


class Player(Shuttle):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.bullets = []
        self.cool_down_counter = 0
        self.shuttle_image = player_icon
        self.bullet_image = enery_circle
        self.mask = pygame.mask.from_surface(self.shuttle_image)
        self.is_alive = True

    def shoot(self, enemy):
            bullet = Bullet(self.x, self.y, self.bullet_image, enemy)
            self.bullets.append(bullet)

    def moveBullets(self, speed):
        for bullet in self.bullets:
            bullet.move(speed)
            if bullet.isBulletCollision(bullet.chosen_enemy):
                
                #chỗ này thêm âm thanh và hiệu ứng nổ khi đạn đụng trúng enemy
                
                bullet.chosen_enemy.health -= 1
                self.bullets.remove(bullet)


    def draw(self):
        super().draw()
        for bullet in self.bullets:
            bullet.draw()

class Enemy(Shuttle):
    def __init__(self, x, y, randomword):
        super().__init__(x, y)
        self.shuttle_image = small_enemy
        self.mask = pygame.mask.from_surface(self.shuttle_image)
        self.word = randomword
        self.health = len(self.word)
        self.color = modern_grey

    def draw(self):
        super().draw()
        text = font.render(self.word, False, (255, 255, 255))
        text_w, text_h = text.get_size()
        if self.color != None:
                pygame.draw.rect(screen, modern_grey, pygame.Rect(self.x + self.getWidth() / 2 - text_w / 2 - 8, self.y - text_h - 8, text_w + 8, text_h + 8), 0, 3)
        if self.health != 0:
                screen.blit(text, (self.x + self.getWidth() / 2 - text_w / 2, self.y - text_h))

    def move(self, player, speed):
        unit_x, unit_y = player.x - self.x, player.y - self.y
        dist = math.hypot(unit_x, unit_y)
        unit_x, unit_y = unit_x / dist, unit_y / dist
        self.x += unit_x * speed
        self.y += unit_y * speed



def runGame():

    pygame.display.set_caption("Z-Type")

    current_enemy_index = 0
    running = True
    FPS = 60
    level = 3
    main_font = pygame.font.SysFont("Calibri", 50)
    lost_font = pygame.font.SysFont("Calibri", 60)

    enemies = []
    wave_length = 2
    enemy_speed = 0.6
    energy_circle_speed = 10

    player = Player(0, 0)
    player.x = WIDTH / 2 - player.getWidth() / 2
    player.y = HEIGHT - player.getHeight()

    clock = pygame.time.Clock()

    lost = False
    lost_screen_duration = 0

    def drawBoard():
        screen.blit(background, (0,0))
        nth_wave = main_font.render(f"Wave: {level - 3}", 1, (255,255,255))
        screen.blit(nth_wave, ((WIDTH - nth_wave.get_width()) / 2, 10))
        for enemy in enemies:
            enemy.draw()
        player.draw()
        if lost:
            '''pygame.mixer.music.pause()'''
            lost_label = lost_font.render("You loser:)", 1, (255,255,255))
            screen.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 350))
        pygame.display.update()

    while running:
        clock.tick(FPS)

        drawBoard()

        if not player.is_alive:
            lost = True
            lost_screen_duration += 1
        if lost:
            if lost_screen_duration > FPS * 3:
                running = False
            else:
                continue

        flag = True
        for enemy in enemies:
            if (enemy.word != ""):
                flag = False
                break
        if flag:
            level += 1
            wave_length += 2

            for i in range(wave_length):
                lines = open(os.path.realpath(f"word_list/{level}_chars/{chr(i + 97)}.txt")).read().splitlines()
                enemy = Enemy(random.randrange(-100, WIDTH + 100), random.randrange(-200, -100), random.choice(lines))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if current_enemy_index == 0:
                    for i in range(len(enemies)):
                        if i >= len(enemies):
                            continue
                        if enemies[i].word == "":
                            continue
                        if (event.key == ord(enemies[i].word[0])):
                            current_enemy_index = -1
                            enemies.append(enemies.pop(i))
                            player.shoot(enemies[current_enemy_index])
                            enemies[current_enemy_index].word = enemies[current_enemy_index].word[1 : ]
                            if enemies[current_enemy_index].word == "":
                                enemies[current_enemy_index].color = None
                                current_enemy_index = 0
                            break
                else:
                    if event.key == ord(enemies[current_enemy_index].word[0]):
                        player.shoot(enemies[current_enemy_index])
                        enemies[current_enemy_index].word = enemies[current_enemy_index].word[1 : ]
                        if enemies[current_enemy_index].word == "":
                            enemies[current_enemy_index].color = None
                            current_enemy_index = 0

        for enemy in enemies[:]:
            if enemy.health != 0:
                enemy.move(player, enemy_speed)
            if isObjsCollision(enemy, player):
                #Chỗ này thêm âm thanh và hiệu ứng nổ khi bị thua (enemy đụng trúng player)
                
                player.is_alive = False
            elif enemy.health == 0:
                if enemy.shuttle_image != hidden_thing:
                    enemy.shuttle_image = hidden_thing
        '''def image_draw(self, url, xLocal, yLocal, xImg, yImg):  # In ra người hình ảnh
         PlanesImg = pygame.image.load(url)
         PlanesImg = pygame.transform.scale(
            PlanesImg, (xImg, yImg))  # change size image
        self.screen.blit(PlanesImg, (xLocal, yLocal))'''

        player.moveBullets(energy_circle_speed)

#button class
class Button():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button on screen
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action

def menu():
    menu_running = True

    music.musicGame(menu_running, False)

    menu_bg = pygame.image.load('image/menu_background.jfif')
    menu_bg = pygame.transform.scale(menu_bg, (WIDTH, HEIGHT))

    main_menu = pygame.image.load('image/main_menu.png')
    main_menu = pygame.transform.scale(main_menu, (430, 120))

    menu_start_btn = pygame.image.load('image/start_menu.png').convert_alpha()
    # menu_start_btn = pygame.transform.scale(menu_start_btn, (280, 112))
    menu_exit_btn = pygame.image.load('image/exit_menu.png').convert_alpha()
    # menu_exit_btn = pygame.transform.scale(menu_exit_btn, (240, 110))

    start_button = Button(25, 300, menu_start_btn, 0.8)
    exit_button = Button(100, 430, menu_exit_btn, 0.6)

    # welcome_img = pygame.image.load('image/welcome.png')
    # welcome_img = Button(60, 255, welcome_img, 0.2)

    gura_img = pygame.image.load('image/gura_menu.png')
    gura_img = Button(240, 225, gura_img, 0.2)
    gura2_img = pygame.image.load('image/gura2_menu.png')
    gura2_img = Button(65, 450, gura2_img, 0.1)

    #==========SETTING==========
    setting_running = False
    check_settting_btn = False

    color_setting = (230, 230, 250)
    surface_setting = pygame.display.set_mode((WIDTH, HEIGHT))

    back_img = pygame.image.load('image/back_button.png')
    back_setting_button = Button(270, 590, back_img, 0.3)

    menu_setting_btn = pygame.image.load('image/setting_btn.png')
    setting_button = Button(360, 580, menu_setting_btn, 0.08)

    #===========Credit==========
    credits_running = False

    color_credits = (54, 69, 79)
    surface_credits = pygame.display.set_mode((WIDTH, HEIGHT))

    back_credits_button = Button(270, 590, back_img, 0.3)

    menu_credits_btn = pygame.image.load('image/credit_button.png')
    credits_button = Button(102, 530, menu_credits_btn, 0.5)

    main_running = True
    while main_running:
        ############################
        #BLIT giao diện mở đầu ở đây
        #NEW GAME
        # QUIT
        if (menu_running == True):
            pygame.display.set_caption("MAIN MENU")
            screen.blit(menu_bg, (0,0))
            screen.blit(main_menu, (0, 10))

            start_button.draw(screen)
            exit_button.draw(screen)
            setting_button.draw(screen)
            credits_button.draw(screen)

            # welcome_img.draw(screen)
            gura_img.draw(screen)
            gura2_img.draw(screen)

        if (setting_running == True):
            pygame.display.set_caption("SETTING")   
            surface_setting.fill(color_setting)
            back_setting_button.draw(screen)

        if (credits_running == True):
            pygame.display.set_caption("CREDITS")
            surface_credits.fill(color_credits)
            back_credits_button.draw(screen)
        ############################
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_running = False

            x, y = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if check_settting_btn == False:
                #Chỗ này thay bằng if <ẤN VÀO NÚT NEW GAME>#
                    if start_button.rect.collidepoint(x, y):
                        menu_running = False
                        game_running = True #đánh dấu đã thoát menu, vào game chơi
                        music.musicGame(menu_running, game_running)
                        runGame()

                    #thêm dòng if ấn vào nút QUIT thì pygame.quit()
                    if exit_button.rect.collidepoint(x, y):
                        main_running = False

                    if setting_button.rect.collidepoint(x, y):
                        check_settting_btn = True
                        setting_running = True
                        menu_running = False

                    if credits_button.rect.collidepoint(x, y):
                        check_settting_btn = True
                        credits_running = True
                        menu_running = False

                # Setting
                elif check_settting_btn == True:
                    if back_setting_button.rect.collidepoint(x, y):
                        menu_running = True
                        setting_running = False
                        check_settting_btn = False
                    if back_credits_button.rect.collidepoint(x, y):
                        menu_running = True
                        credits_running = False
                        check_settting_btn = False
                     
menu()