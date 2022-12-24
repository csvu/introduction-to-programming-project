import pygame, math, os, time, random
from sound import music #từ sound.py móc class music ra
#from numpy import log2, power #tai thu vien numpy bang cach vao terminal gõ pip install numpy rồi nhấn enter.


pygame.init()

BLACK = (0,0,0)

WIDTH, HEIGHT = 430, 650

lost = False
to_rungame = False
win = False   
duration = 0

white = (255, 255, 255)
modern_grey = (42, 42, 42)
mustard_yellow = (255, 219, 88)

screen = pygame.display.set_mode((WIDTH, HEIGHT))

#===========Fonts 8Bits===========
font_8bits_title_main_menu = pygame.font.Font("fonts/pixeboy-font/Pixeboy-z8XGD.ttf", 86) # dành cho cỡ chữ như main menu
font_8bits_small = pygame.font.Font("fonts/pixeboy-font/Pixeboy-z8XGD.ttf", 24) # dành cho cỡ chữ small
font_8bits = pygame.font.Font("fonts/pixeboy-font/Pixeboy-z8XGD.ttf", 32) # dành cho cỡ chữ thường
font_8bits_medium = pygame.font.Font("fonts/pixeboy-font/Pixeboy-z8XGD.ttf", 48) # dành cho cỡ chữ medium
font_8bits_title = pygame.font.Font("fonts/pixeboy-font/Pixeboy-z8XGD.ttf", 86) # dành cho cỡ chữ credits và paused
#=================================

boss_image = pygame.image.load(os.path.realpath("image/boss.png"))
small_enemy = pygame.image.load(os.path.realpath("image/small_enemy3.png"))
player_icon = pygame.image.load(os.path.realpath("image/player_icon2.png"))
enery_circle = pygame.image.load(os.path.relpath("image/energy_circle3.png"))
hidden_thing = pygame.image.load(os.path.realpath("image/hidden_thing.png"))
background = pygame.image.load(os.path.realpath("image/background7.png"))



font = pygame.font.SysFont("Calibri", 20, True)

all_explosions = pygame.sprite.Group()


explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
for i in range (2) :
                    filename = 'explosion{}.png' .format(i)
                    img = pygame.image.load (os.path.join("image", filename)).convert_alpha()
                    img.set_colorkey (BLACK)
                    img_lg = pygame.transform.scale (img, (75,75))
                    explosion_anim ['lg'].append (img_lg)
                    img_sm = pygame. transform.scale (img , (32,32))
                    explosion_anim ['sm'].append (img_sm)

class Explosion1 (pygame.sprite.Sprite):
    def __init__(self, center, size) : 
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim [self.size][0]
        self.rect = self.image.get_rect ()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 80

    def update (self) :
        now = pygame.time.get_ticks ()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len (explosion_anim[self.size]) :
                self.kill()
            else :
                center = self.rect.center
                self.image = explosion_anim [self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
          

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


def isObjsCollision(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def explosion(screen, color, position):
    Blast = []
    for i in range(1, 6):
        Blast.append(pygame.image.load("image/exp" + str(i) + ".png"))
    print(len(Blast))

    for i in range(1, 60, 1):
        screen.blit(background, (0,0))
        if (i < 25):
            HalfWidth = int(Blast[int(i/5)].get_width()/2)
            HalfHeight = Blast[int(i/5)].get_height()/2
            screen.blit(Blast[int(i/5)], (position[0] - HalfWidth, int(position[1] - HalfHeight)))
        pygame.draw.circle(screen, (70, 163, 141), position , int(math.pow(i, 2.2)), int(4/3*math.log2(i)))
        pygame.display.flip()
        pygame.time.delay(60)

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
        self.all_explosions = pygame.sprite.Group()
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
                expl = Explosion1 (((bullet.x - (bullet.image.get_width() / 2) + 35),(bullet.y - (bullet.image.get_height() / 2)+20)), 'sm')
                #all_explosions.add(expl)
                self.all_explosions.add(expl)
                bullet.chosen_enemy.health -= 1
                if (bullet.chosen_enemy.health == 0):
                    expl = Explosion1 (((bullet.x - (bullet.image.get_width() / 2) + 40),(bullet.y - (bullet.image.get_height() / 2))), 'lg')
                    #all_explosions.add(expl)
                    self.all_explosions.add(expl)

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
        self.text_color = white
        self.color = modern_grey

    def draw(self):
        super().draw()
        text = font.render(self.word, False, self.text_color)
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

  
#===========Pause Game==========

def paused():
    paused_game = True

    color_paused = (237, 234, 222)

    paused_title = font_8bits_title.render('Pausing', False, (0, 0, 0))
    press_continue = font_8bits.render('Press Esc to continue...', False, (0, 0, 0))


    back_to_menu_img = pygame.image.load('image/back_to_menu_button.png')
    back_paused_button = Button(190, 590, back_to_menu_img, 0.3)
    
    while paused_game:
        screen.fill((color_paused))
        screen.blit(paused_title, (WIDTH // 2 - (paused_title.get_width()) // 2, 20))
        screen.blit(press_continue, ((WIDTH // 2 - (press_continue.get_width()) // 2, 550)))
        back_paused_button.draw(screen)
        pygame.display.flip()

        x, y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused_game = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_paused_button.rect.collidepoint(x, y):
                    paused_game = False
                    menu()



#==========Hien thi man hinh khi ban die - END GAME==========
def showLost():
        show_lost = True
        lost_color_bg = (105,105,105)
        lost_announcement = font_8bits_title.render('Loser', False, (255, 255, 255,))
        lost_announcement_footer = font_8bits.render('Con   cai   nit !!! :)', False, (255, 255, 255,))

        back_to_menu_img = pygame.image.load('image/back_to_menu_button.png')
        back_to_menu_button = Button(60, (HEIGHT // 1.5 - (back_to_menu_img.get_height()) // 1.5 ), back_to_menu_img, 0.4)

        replay_img = pygame.image.load('image/replay_buttonn.png')
        replay_button = Button(50, (HEIGHT // 2 - (replay_img.get_height()) // 2 ), replay_img, 0.4)

        while show_lost:
                screen.fill(lost_color_bg)
                screen.blit(lost_announcement, ((WIDTH // 2 - (lost_announcement.get_width()) // 2), 20))
                screen.blit(lost_announcement_footer, ((WIDTH // 2 - (lost_announcement_footer.get_width()) // 2), 600))
                back_to_menu_button.draw(screen)
                replay_button.draw(screen)
                pygame.display.flip()

                x, y = pygame.mouse.get_pos()

                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                quit()
                        '''
                        if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_q:
                                        quit()
                        '''
                        if event.type == pygame.MOUSEBUTTONDOWN:
                                if back_to_menu_button.rect.collidepoint(x, y):
                                        show_lost = False
                                        print('x')
                                elif replay_button.rect.collidepoint(x, y):
                                        #Dành cho Tùng
                                        global to_rungame
                                        to_rungame = True
                                        print('y')
                                        show_lost = False

#====================================================================


#==========Hien thi man hinh khi ban thang - WINWIN GAME==========
def showWin():
        show_win = True

        #===========================My Gura===========================

        gura1_win_img = pygame.image.load('image/gura1_winwin.png')
        gura1_win_img = Button(50, 300, gura1_win_img, 0.2)

        gura2_win_img = pygame.image.load('image/gura2_winwin.png')
        gura2_win_img = Button(280, 500, gura2_win_img, 0.2)

        gura3_win_img = pygame.image.load('image/gura3_winwin.png')
        gura3_win_img = Button(170, 170, gura3_win_img, 0.3)

        #===============================================================

        win_color_bg = (250,160,160)
        win_announcement = font_8bits_medium.render('You have proved', False, (0, 0, 0,))
        win_sub_announcement = font_8bits_medium.render('You are not a Loser', False, (0, 0, 0,))
        win_announcement_footer = font_8bits.render('Congratulations !!!', False, (0, 0, 0,))

        back_to_menu_img = pygame.image.load('image/back_to_menu_button.png')
        back_to_menu_button = Button(60, (HEIGHT // 1 - (back_to_menu_img.get_height()) // 1 ), back_to_menu_img, 0.4)

        replay_img = pygame.image.load('image/replay_buttonn.png')
        replay_button = Button(50, (HEIGHT // 1.1 - (replay_img.get_height()) // 1.1 ), replay_img, 0.4)

        #=====DURATION=====
        show_duration_announcement = font_8bits_small.render('You beat this game in ' + str(duration) + ' seconds', False, (0,0,0))
        #==================

        while show_win:
                screen.fill(win_color_bg)

                gura1_win_img.draw(screen)
                gura3_win_img.draw(screen)

                screen.blit(win_announcement, ((WIDTH // 2 - (win_announcement.get_width()) // 2), 30))
                screen.blit(win_sub_announcement, ((WIDTH // 2 - (win_sub_announcement.get_width()) // 2), 80))
                back_to_menu_button.draw(screen)
                replay_button.draw(screen)
                gura2_win_img.draw(screen)
                screen.blit(win_announcement_footer, ((WIDTH // 2 - (win_announcement_footer.get_width()) // 2), 600))
                screen.blit(show_duration_announcement, ((WIDTH // 2 - (show_duration_announcement.get_width()) // 2), 170))
                pygame.display.flip()

                x, y = pygame.mouse.get_pos()

                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                quit()
                        '''
                        if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_q:
                                        quit()
                        '''
                        if event.type == pygame.MOUSEBUTTONDOWN:
                                if back_to_menu_button.rect.collidepoint(x, y):
                                        show_win = False
                                        print('x')
                                elif replay_button.rect.collidepoint(x, y):
                                        #Dành cho Tùng
                                        global to_rungame
                                        to_rungame = True
                                        print('y')
                                        show_win = False

#====================================================================


def runGame():

    pygame.display.set_caption("A mishmash")

    current_enemy_index = 0
    running = True
    FPS = 60
    level = 3
    main_font = pygame.font.SysFont("Calibri", 50)

    enemies = []
    wave_length = 2
    boss_speed = 0.2
    enemy_speed = 0.6
    energy_circle_speed = 10

    player = Player(0, 0)
    player.x = WIDTH / 2 - player.getWidth() / 2
    player.y = HEIGHT - player.getHeight() - 10
    boss = Enemy(WIDTH / 2 - boss_image.get_width() / 2, boss_image.get_height() + 10, "IVeryLov3Ron@ld0&YoU")
    boss_live = 0
    boss.shuttle_image = boss_image

    start = pygame.time.get_ticks()
    clock = pygame.time.Clock()

    def drawBoard():
        screen.blit(background, (0, 0))
        nth_wave = font_8bits.render(f"Wave: {level - 3}", 1, (255,255,255))
        screen.blit(nth_wave, ((WIDTH - nth_wave.get_width()) / 2, 10))
        for enemy in enemies:
            enemy.draw()
        player.draw()
        if level == 9:
                boss.draw()
        player.all_explosions.draw(screen)
        '''
        if lost:
            pygame.mixer.music.pause()
            lost_label = lost_font.render("You loser:)", 1, (255,255,255))
            screen.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 350))
        '''
        pygame.display.update()
        
        #def draw():
        #    screen.blit(self.image,(self.x, self.y)) 
      
    while running:
        

        clock.tick(FPS)

        drawBoard()

        flag = True
        for enemy in enemies:
            if (enemy.word != ""):
                flag = False
                break


        if flag:
            if (level != 9):
                level += 1
            wave_length += 1
            if (level == 8):
                level += 1
                wave_length = 2

        
            for i in range(wave_length):
                lines = open(os.path.realpath(f"word_list/{level}_chars/{chr(i + 97)}.txt")).read().splitlines()
                enemy = Enemy(2 * i * small_enemy.get_width() - 100, random.randrange(-150, -100), random.choice(lines))
                enemies.append(enemy)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            
            if event.type == pygame.KEYDOWN:
                print (event)
                if (level == 9 and boss.word != "" and current_enemy_index == 0):
                        if (event.unicode == boss.word[0]):
                                player.shoot(boss)
                                boss.word = boss.word[1 : ]
                if current_enemy_index == 0:
                    for i in range(len(enemies)):
                        if i >= len(enemies):
                            continue
                        if enemies[i].word == "":
                            continue
                        if (event.key == ord(enemies[i].word[0]) and 0 <= enemies[i].x <= WIDTH and 0 <= enemies[i].y <= HEIGHT):
                            current_enemy_index = -1
                            enemies[i].text_color = mustard_yellow
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
                if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE: # Nhan vao Enter hoac Esc thi Paused Game
                        paused() 

        global lost
        if (level == 9):
                boss.move(player, boss_speed)
        if isObjsCollision(boss, player):
                music.soundEffect()
                explosion(screen, (100, 500, 500), (player.x, player.y))
                #player.is_alive = False
                lost = True
                return

        for enemy in enemies[:]:
            if enemy.health != 0:
                enemy.move(player, enemy_speed)
            if isObjsCollision(enemy, player):
                music.soundEffect()
                explosion(screen, (100, 500, 500), (player.x, player.y))
                #player.is_alive = False
                lost = True
                return
            elif enemy.health == 0:
                if enemy.shuttle_image != hidden_thing:
                    enemy.shuttle_image = hidden_thing
                #chỗ này thêm âm thanh và hiệu ứng nổ khi đạn đụng trúng enemy
                
               
               

        '''def image_draw(self, url, xLocal, yLocal, xImg, yImg):  # In ra người hình ảnh
         PlanesImg = pygame.image.load(url)
         PlanesImg = pygame.transform.scale(
            PlanesImg, (xImg, yImg))   change size image
        self.screen.blit(PlanesImg, (xLocal, yLocal))'''

        player.moveBullets(energy_circle_speed)
        
        player.all_explosions.update()
        if (boss.health == 0):
                if boss_live == 1:
                        global win
                        win = True
                        global duration
                        duration = (pygame.time.get_ticks() - start) // 1000
                        print(duration)
                        return
                else:
                        boss_live += 1
                        boss.word = "ABCDEFG" 
                        boss.health = len(boss.word)

def menu():
    menu_running = True

    music.musicGame(menu_running, False)

    menu_bg = pygame.image.load('image/menu_background.jfif')
    menu_bg = pygame.transform.scale(menu_bg, (WIDTH, HEIGHT))

    # main_menu = pygame.image.load('image/main_menu.png')
    # main_menu = pygame.transform.scale(main_menu, (430, 120))

    menu_start_btn = pygame.image.load('image/start_menu.png').convert_alpha()
    
    menu_exit_btn = pygame.image.load('image/exit_menu.png').convert_alpha()

    start_button = Button(25, 300, menu_start_btn, 0.8)
    exit_button = Button(100, 430, menu_exit_btn, 0.6)

    gura_img = pygame.image.load('image/gura_menu.png')
    gura_img = Button(240, 225, gura_img, 0.2)
    gura2_img = pygame.image.load('image/gura2_menu.png')
    gura2_img = Button(65, 450, gura2_img, 0.1)

    title_main_menu = font_8bits_title_main_menu.render('A mishmash', False, (255, 192, 0))
    title_width = title_main_menu.get_width()
    title_height = title_main_menu.get_height()
    x_title = WIDTH // 2 - title_width // 2
    y_title = HEIGHT // 10 - title_height // 10
    
    #==========SETTING==========
    setting_running = False
    check_settting_btn = False

    color_setting = (230, 230, 250)
    surface_setting = pygame.display.set_mode((WIDTH, HEIGHT))

    back_img = pygame.image.load('image/back_button.png')
    back_setting_button = Button(290, 590, back_img, 0.3)

    menu_setting_btn = pygame.image.load('image/setting_btn.png')
    setting_button = Button(360, 580, menu_setting_btn, 0.08)

    #===========Credit==========
    credits_running = False

    color_credits = (54, 69, 79)
    surface_credits = pygame.display.set_mode((WIDTH, HEIGHT))

    back_credits_button = Button(290, 590, back_img, 0.3)

    menu_credits_btn = pygame.image.load('image/credit_button.png')
    credits_button = Button(102, 530, menu_credits_btn, 0.5)

    credits_team = font_8bits_title.render('Nhom 3', False, (255, 192, 0))
    credits_1= font_8bits.render('Ngo Van Khai: 22127174_Leader', False, (255, 255, 255))
    credits_2= font_8bits.render('Dang Nguyen Vu: 22127461', False, (255, 255, 255))
    credits_3= font_8bits.render('Le Thi Thanh Thuy: 22127411', False, (255, 255, 255))
    credits_4= font_8bits.render('Tran Thi My Y: 22127468', False, (255, 255, 255))
    credits_5= font_8bits.render('To Quoc Thanh: 22127388', False, (255, 255, 255))
    credits_6= font_8bits.render('Thai Huyen Tung: 22127441', False, (255, 255, 255))
    credits_music = font_8bits.render('Music:', False, (255, 192, 0))
    credits_name = font_8bits.render('Nishiki Yasunori', False, (255, 255, 255))

    main_running = True
    while main_running:
        ############################
        #BLIT giao diện mở đầu ở đây
        #NEW GAME
        # QUIT

        #lost screen
        #Dành cho Tùng 
        global lost
        global to_rungame
        while lost:
                print('ccc')
                showLost()
                if to_rungame:
                        to_rungame = False
                        lost = False
                        music.musicGame(menu_running, game_running)
                        runGame()
                else:
                        menu_running = True
                        music.musicGame(menu_running, False)
                        lost = False
                        print('bbb')
        #Dành cho Tùng

        global win
        while win:
                showWin()
                if to_rungame:
                        to_rungame = False
                        win = False
                        music.musicGame(menu_running, game_running)
                        runGame()
                else:
                        menu_running = True
                        music.musicGame(menu_running, False)
                        win = False
                        print('bbb')


        #print('ddd')
        #print(menu_running)
        if (menu_running == True):
            pygame.display.set_caption("MAIN MENU")
            print('aaa')
            screen.blit(menu_bg, (0,0))
            screen.blit(title_main_menu, (x_title, y_title))
            # screen.blit(main_menu, (0, 10))

            start_button.draw(screen)
            exit_button.draw(screen)
            setting_button.draw(screen)
            credits_button.draw(screen)

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
            
            pygame.draw.rect(screen, (93, 63, 211), pygame.Rect((WIDTH // 2 - (credits_team.get_width()) // 2 - 12, 40, (credits_team.get_width()) + 20, 70)), 0, 10)

            screen.blit(credits_team, ((WIDTH // 2 - (credits_team.get_width()) // 2, 50)))
            screen.blit(credits_1, ((WIDTH // 2 - (credits_1.get_width()) // 2, 150)))
            screen.blit(credits_2, ((WIDTH // 2 - (credits_2.get_width()) // 2, 200)))
            screen.blit(credits_3, ((WIDTH // 2 - (credits_3.get_width()) // 2, 250)))
            screen.blit(credits_4, ((WIDTH // 2 - (credits_4.get_width()) // 2, 300)))
            screen.blit(credits_5, ((WIDTH // 2 - (credits_5.get_width()) // 2, 350)))
            screen.blit(credits_6, ((WIDTH // 2 - (credits_6.get_width()) // 2, 400)))
            screen.blit(credits_music, ((WIDTH // 2 - (credits_music.get_width()) // 2, 450)))
            screen.blit(credits_name, ((WIDTH // 2 - (credits_name.get_width()) // 2, 500)))

        
        # if (paused == True):
        #     pass
        ############################
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

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
                        quit()

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
