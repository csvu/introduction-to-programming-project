import pygame, math, os, time, random, string, sys
from sound import music #từ sound.py móc class music ra


pygame.init()

BLACK = (0,0,0)

WIDTH, HEIGHT = 430, 650

lost = False
to_rungame = False
win = False

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
small_enemy = pygame.image.load(os.path.realpath("image/small_enemy5.png"))
player_icon = pygame.image.load(os.path.realpath("image/player_icon.png"))
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

def explosion(screen, color, position, scroll): #tàu ta nổ hay tàu boss nổ
    Blast = []
    for i in range(1, 31):
        Blast.append(pygame.image.load("image/guivu/" + str(i) + ".png"))

    for i in range(1, 60, 1):
        for j in range (1, 3):
                screen.blit(background, (0, HEIGHT - j * background.get_height() + scroll))
        HalfWidth = int(Blast[int(i/2)].get_width()/2)
        HalfHeight = Blast[int(i/2)].get_height()/2
        screen.blit(Blast[int(i/2)], (position[0] - HalfWidth, int(position[1] - HalfHeight)))
        pygame.draw.circle(screen, (70, 163, 141), position , int(math.pow(i, 2.2)), int(4/3*math.log2(i)))
        pygame.display.flip()
        pygame.time.delay(17)
    pygame.time.delay(1500)


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
            bullet = Bullet(WIDTH / 2 - self.bullet_image.get_width() / 2, self.y, self.bullet_image, enemy)
            self.bullets.append(bullet)

    def moveBullets(self, speed):
        for bullet in self.bullets:
            bullet.move(speed)
            if bullet.isBulletCollision(bullet.chosen_enemy):
                expl = Explosion1 (((bullet.x - (bullet.image.get_width() / 2) + 35),(bullet.y - (bullet.image.get_height() / 2)+20)), 'sm')
                self.all_explosions.add(expl)
                bullet.chosen_enemy.health -= 1
                if (bullet.chosen_enemy.health == 0):
                    expl = Explosion1 (((bullet.x - (bullet.image.get_width() / 2) + 40),(bullet.y - (bullet.image.get_height() / 2))), 'lg')
                    self.all_explosions.add(expl)
                    music.soundEffect(enemy_explosion = True)

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
                pygame.draw.rect(screen, modern_grey, pygame.Rect(self.x + self.getWidth() / 2 - text_w / 2 - 4, self.y + self.getHeight() - 4, text_w + 8, text_h + 8), 0, 3)
        if self.health != 0:
                screen.blit(text, (self.x + self.getWidth() / 2 - text_w / 2, self.y + self.getHeight()))

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
                #quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused_game = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_paused_button.rect.collidepoint(x, y):
                    music.soundEffect(clicking = True)
                    paused_game = False
                    menu()



#==========Hien thi man hinh khi ban die - END GAME==========
def showLost():
        show_lost = True
        lost_color_bg = (105,105,105)
        lost_announcement = font_8bits_title.render('Loser', False, (255, 255, 255,))
        show_duration_announcement3 = font_8bits.render('Your score: ' + str(score), False, (255,255,255))

        music.musicGame(show_lost = True)

        back_to_menu_img = pygame.image.load('image/back_to_menu_button.png')
        back_to_menu_button = Button(60, (HEIGHT // 1.5 - (back_to_menu_img.get_height()) // 1.5 ), back_to_menu_img, 0.4)

        replay_img = pygame.image.load('image/replay_buttonn.png')
        replay_button = Button(50, (HEIGHT // 2 - (replay_img.get_height()) // 2 ), replay_img, 0.4)

        while show_lost:
                screen.fill(lost_color_bg)
                screen.blit(lost_announcement, ((WIDTH // 2 - (lost_announcement.get_width()) // 2), 20))
                screen.blit(show_duration_announcement3, ((WIDTH // 2 - (show_duration_announcement3.get_width()) // 2), 100))
                back_to_menu_button.draw(screen)
                replay_button.draw(screen)
                pygame.display.flip()

                x, y = pygame.mouse.get_pos()

                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                #quit()
                                sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                                if back_to_menu_button.rect.collidepoint(x, y):
                                        music.soundEffect(clicking = True)
                                        show_lost = False
                                elif replay_button.rect.collidepoint(x, y):
                                        #Dành cho Tùng
                                        global to_rungame
                                        to_rungame = True
                                        show_lost = False

#====================================================================


#==========Hien thi man hinh khi ban thang - WINWIN GAME=============
def showWin():
        show_win = True

        bg_win = pygame.image.load('./image/bg_win.jpg')
        bg_win = pygame.transform.scale(bg_win,(WIDTH, HEIGHT))
        win_announcement = font_8bits_title.render('Congrats !', False, (255, 192, 0))

        music.musicGame(show_win = True)

        replay_img = pygame.image.load('image/replay_buttonn.png')
        replay_button = Button(50, (HEIGHT // 1.2 - (replay_img.get_height()) // 1.2 ), replay_img, 0.4)

        back_to_menu_img = pygame.image.load('image/back_to_menu_button.png')
        back_to_menu_button = Button(60, (HEIGHT // 1 - (back_to_menu_img.get_height()) // 1 ), back_to_menu_img, 0.4)

        #=====DURATION=====
        show_duration_announcement = font_8bits.render('You beat this game', False, (255,255,255))
        show_duration_announcement2 = font_8bits.render('in ' + str(duration) + ' seconds', False, (255,255,255))
        show_duration_announcement3 = font_8bits.render('Your score: ' + str(score), False, (255,255,255))
        #==================

        while show_win:
                screen.blit(bg_win,(0,0))
                screen.blit(win_announcement, ((WIDTH // 2 - (win_announcement.get_width()) // 2), 50))
                screen.blit(show_duration_announcement, ((WIDTH // 2 - (show_duration_announcement.get_width()) // 2), 200))
                screen.blit(show_duration_announcement2, ((WIDTH // 2 - (show_duration_announcement2.get_width()) // 2), 250))
                screen.blit(show_duration_announcement3, ((WIDTH // 2 - (show_duration_announcement3.get_width()) // 2), 300))
                back_to_menu_button.draw(screen)
                replay_button.draw(screen)
                pygame.display.flip()

                x, y = pygame.mouse.get_pos()

                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                                #quit()
                                sys.exit()
                        
                        if event.type == pygame.MOUSEBUTTONDOWN:
                                if back_to_menu_button.rect.collidepoint(x, y):
                                        music.soundEffect(clicking = True)
                                        show_win = False
                                elif replay_button.rect.collidepoint(x, y):
                                        #Dành cho Tùng
                                        global to_rungame
                                        to_rungame = True
                                        show_win = False

#====================================================================


def runGame():
    current_enemy_index = 0
    running = True
    FPS = 60
    level = 3 #level chỉ độ khó của địch. mới khi vào chơi level tăng lên thành 4 tức tàu địch có 4 ký tự
    boss_level = 5
    offset = 0
    global score
    score = 0
    global duration #thời gian của 1 ván chơi
    duration = 0
    global wave_start #thời gian bắt đầu 1 wave
    wave_start = 0
    global wave_key
    wave_key = False
    main_font = pygame.font.SysFont("Calibri", 50)

    enemies = []
    wave_length = 2
    boss_speed = 0.2
    enemy_speed = 0.6
    energy_circle_speed = 15

    player = Player(0, 0)
    player.x = WIDTH / 2 - player.getWidth() / 2
    player.y = HEIGHT - player.getHeight() - 10
    #boss = Enemy(WIDTH / 2 - boss_image.get_width() / 2, -boss_image.get_height() - 10, "IV3RYL@V3ME$$I&YoU")
    boss = Enemy(WIDTH / 2 - boss_image.get_width() / 2, -boss_image.get_height() - 10, "1\/38\|/|_@\/3|\/|3$$1")
    boss_live = 0
    boss.shuttle_image = boss_image

    scroll = 0

    start = pygame.time.get_ticks()
    clock = pygame.time.Clock()

    def drawBoard():
        for i in range (1, 3):
                screen.blit(background, (0, HEIGHT - i * background.get_height() + scroll))
        
        nth_wave = font_8bits.render(f"Wave: {level - 3 if level != 11 else 7}", 1, (255,255,255))
        screen.blit(nth_wave, ((WIDTH - nth_wave.get_width()) // 2, 10))

        done_wave1 = font_8bits.render("Go", True, (255,255,255)) #hiện dòng này khi mới vào chơi
        done_wave2 = font_8bits_small.render("Clear", True, (255,255,255)) # hiện các dòng chữ sau nếu xong 1 wave
        done_wave3 = font_8bits_small.render(f"Your score: {score}", True, (255,255,255))
        done_wave4 = font_8bits_small.render("Warning!", True, (255, 0, 0)) # hiện waring! khi có boss
        if time.time() < wave_start: #hiện chữ trong 2.5 giây
            if level == 4:
                screen.blit( done_wave1, ((WIDTH - done_wave1.get_width()) // 2, (HEIGHT - done_wave1.get_height()) // 2) )
            elif level > 4 and level != 11:
                screen.blit( done_wave2, ((WIDTH - done_wave2.get_width()) // 2, HEIGHT//2 - 3 - done_wave2.get_height()) )
                screen.blit( done_wave3, ((WIDTH - done_wave3.get_width()) // 2, HEIGHT//2 + 3 + done_wave3.get_height()) )
            elif level == 11:
                screen.blit( done_wave4, ((WIDTH - done_wave4.get_width()) // 2, HEIGHT//2 - 3 - done_wave4.get_height()) )
                screen.blit( done_wave3, ((WIDTH - done_wave3.get_width()) // 2, HEIGHT//2 + 3 + done_wave3.get_height()) )
               
        if level == 11:
                boss.draw()
        for enemy in enemies:
            enemy.draw()
        player.draw()
        player.all_explosions.draw(screen)
        
        pygame.display.update()
        
      
    while running:
        clock.tick(FPS)

        drawBoard()

        if scroll >= background.get_height():
                scroll = 0
        scroll += 0.5

        flag = True
        for enemy in enemies:
            if (enemy.word != ""):
                flag = False
                break


        if flag:
            if (level != 11):
                level += 1
                wave_key = True
                wave_start = time.time() + 2.5 #cộng thêm 2.5 để hiện chữ 2.5 giây
            wave_length += 1
            if (level == 10):
                level += 1
                wave_length = 2
                enemy_speed = 0.9
                music.musicGame(game_run = True, game_run_boss = True)
            if (level == 11):
                boss_level += 1



            arr = random.sample(range(26), wave_length) #tạo mảng lưu ký tự khác nhau để các tàu không bị trùng ký tự đầu
            for i in range(wave_length):
                lines = open(os.path.realpath(f"word_list/{min(level, 6)}_chars/{chr(arr[i] + 97)}.txt")).read().splitlines()
                #lines = open(os.path.realpath(f"word_list/{level if level != 11 else boss_level}_chars/{chr(i + 97)}.txt")).read().splitlines()
                enemy = Enemy(((-1) ** offset) * (2 * i * small_enemy.get_width() - 10) + (offset) * WIDTH, random.randrange(-200, -100), random.choice(lines))
                enemies.append(enemy)
            offset ^= 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                event_key_correct = False
                if (level == 11 and boss.word != "" and current_enemy_index == 0):
                        if (event.unicode == boss.word[0]):
                                player.shoot(boss)
                                music.soundEffect(player_shooting = True)
                                score += 1
                                event_key_correct = True
                                boss.word = boss.word[1 : ]
                if current_enemy_index == 0:
                    for i in range(len(enemies)):
                        if i >= len(enemies):
                            continue
                        if enemies[i].word == "":
                            continue
                        if (event.unicode == enemies[i].word[0] and 0 <= enemies[i].x <= WIDTH and enemies[i].y >= -enemies[i].getHeight()):
                            music.soundEffect(player_shooting = True)
                            score += 1
                            event_key_correct = True
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
                    if event.unicode == enemies[current_enemy_index].word[0]:
                        music.soundEffect(player_shooting = True)
                        score += 1
                        event_key_correct = True
                        player.shoot(enemies[current_enemy_index])
                        enemies[current_enemy_index].word = enemies[current_enemy_index].word[1 : ]
                        if enemies[current_enemy_index].word == "":
                            enemies[current_enemy_index].color = None
                            current_enemy_index = 0
                if boss.word != "":
                        if (event.key != pygame.K_ESCAPE and event_key_correct != True and level < 11) or (event.unicode != boss.word[0] and event_key_correct != True and level == 11):
                                music.soundEffect(player_type_wrong = True)
                                score -= 1
                #Nhan vao Esc thi Paused Game
                if event.key == pygame.K_ESCAPE:
                        paused() 

        global lost
        if (level == 11):
                boss.move(player, boss_speed)
        if isObjsCollision(boss, player):
                music.soundEffect(player_explosion = True)
                explosion(screen, (100, 500, 500), (WIDTH / 2, player.y), scroll)
                lost = True
                return

        for enemy in enemies[:]:
            if enemy.health != 0:
                enemy.move(player, enemy_speed)
            if isObjsCollision(enemy, player):
                music.soundEffect(player_explosion = True)
                explosion(screen, (100, 500, 500), (WIDTH / 2, player.y), scroll)
                lost = True
                return
            elif enemy.health == 0:
                if enemy.shuttle_image != hidden_thing:
                    enemy.shuttle_image = hidden_thing
                
               
               
        player.moveBullets(energy_circle_speed)
        
        player.all_explosions.update()
        if (boss.health == 0):
                if boss_live == 1:
                        music.soundEffect(player_explosion = True)
                        explosion(screen, (100, 500, 500), (WIDTH / 2, boss.y + 20), scroll)
                        global win
                        win = True
                        duration = (pygame.time.get_ticks() - start) // 1000 #thời gian đã chơi nếu thắng (tính cả thời gian tạm dừng game)
                        return
                else:
                        boss_live += 1
                        #boss.word = "AC&)!^G$%+&AND*#YOU%^!_WIN! 6@|*|*\|/|\|3\/\/\|/3@8"
                        boss.word = "6@|*|*\|/|\|3\/\/\|/3@8" 
                        boss.health = len(boss.word)

def menu():
    pygame.display.set_caption("AliType")
    menu_running = True

    music.musicGame(menu_running = True)

    menu_bg = pygame.image.load('image/menu_background.jfif')
    menu_bg = pygame.transform.scale(menu_bg, (WIDTH, HEIGHT))

    menu_start_btn = pygame.image.load('image/start_menu.png').convert_alpha()
    
    menu_exit_btn = pygame.image.load('image/exit_menu.png').convert_alpha()

    start_button = Button(25, 300, menu_start_btn, 0.8)
    exit_button = Button(100, 430, menu_exit_btn, 0.6)

    title_main_menu = font_8bits_title_main_menu.render("AliType", False, (255, 192, 0))
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
    setting_button = Button(360, 580, menu_setting_btn, 0.4)

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
        global lost
        global to_rungame
        while lost:
                showLost()
                if to_rungame:
                        to_rungame = False
                        lost = False
                        music.musicGame(game_run = True)
                        runGame()
                else:
                        menu_running = True
                        music.musicGame(menu_running = True)
                        lost = False

        global win
        while win:
                showWin()
                if to_rungame:
                        to_rungame = False
                        win = False
                        music.musicGame(game_run = True)
                        runGame()
                else:
                        menu_running = True
                        music.musicGame(menu_running = True)
                        win = False


        if (menu_running == True):
            screen.blit(menu_bg, (0,0))
            screen.blit(title_main_menu, (x_title, y_title))

            start_button.draw(screen)
            exit_button.draw(screen)
            setting_button.draw(screen)
            credits_button.draw(screen)

        if (setting_running == True):
            surface_setting.fill(color_setting)

            volume = music.displayVolumeSetting()
            volume_sound = music.displaySoundSetting()

            setting_line = font_8bits_title.render("Setting", False, (255, 192, 0))
            music_line= font_8bits_medium.render("Music", False, (0, 0, 0))
            show_music = font_8bits_medium.render(str(volume), False, (0, 0, 0))
            sound_line= font_8bits_medium.render("Sound", False, (0, 0, 0))
            show_sound = font_8bits_medium.render(str(volume_sound), False, (0, 0, 0))

            add_img = pygame.image.load("image/add_button.png")
            add_volume_button = Button(115, 225, add_img, 0.3)
            add_sound_button = Button(115, 400, add_img, 0.3)
            minus_img = pygame.image.load("image/minus_button.png")
            minus_volume_button = Button(315 - minus_img.get_width()*0.3, 225, minus_img, 0.3)
            minus_sound_button = Button(315 - minus_img.get_width()*0.3, 400, minus_img, 0.3)
    
            back_img = pygame.image.load('image/back_button.png')
            back_setting_button = Button(290, 590, back_img, 0.3)

            screen.blit(setting_line, ((WIDTH // 2 - (setting_line.get_width()) // 2, 50)))
            screen.blit(music_line, ((WIDTH // 2 - (music_line.get_width()) // 2, 180)))
            screen.blit(show_music, ((WIDTH // 2 - (show_music.get_width()) // 2), 235))
            screen.blit(sound_line, ((WIDTH // 2 - (sound_line.get_width()) // 2, 355)))
            screen.blit(show_sound, ((WIDTH // 2 - (show_sound.get_width()) // 2), 410))

            add_volume_button.draw(screen)
            minus_volume_button.draw(screen)
            add_sound_button.draw(screen)
            minus_sound_button.draw(screen)
            back_setting_button.draw(screen)
            
            pygame.display.flip()
            x, y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    #quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if add_volume_button.rect.collidepoint(x, y):
                        music.musicSetting(add_volume = True)
                        music.soundEffect(clicking = True)
                    if minus_volume_button.rect.collidepoint(x, y):
                        music.musicSetting(minus_volume = True)
                        music.soundEffect(clicking = True)
                    if add_sound_button.rect.collidepoint(x, y):
                        music.musicSetting(add_sound = True)
                        music.soundEffect(clicking = True)
                    if minus_sound_button.rect.collidepoint(x, y):
                        music.musicSetting(minus_sound = True)
                        music.soundEffect(clicking = True)
                    if back_setting_button.rect.collidepoint(x, y):
                        music.soundEffect(clicking = True)
                        menu_running = True
                        setting_running = False
                        check_settting_btn = False

        if (credits_running == True):
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


        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #quit()
                sys.exit()

            x, y = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if check_settting_btn == False:
                    if start_button.rect.collidepoint(x, y):
                        menu_running = False
                        game_running = True
                        music.musicGame(game_run = True)
                        runGame()

                    #thêm dòng if ấn vào nút QUIT thì pygame.quit()
                    if exit_button.rect.collidepoint(x, y):
                        #quit()
                        sys.exit()

                    if setting_button.rect.collidepoint(x, y):
                        music.soundEffect(clicking = True)
                        check_settting_btn = True
                        setting_running = True
                        menu_running = False

                    if credits_button.rect.collidepoint(x, y):
                        music.soundEffect(clicking = True)
                        check_settting_btn = True
                        credits_running = True
                        menu_running = False

                # Setting
                elif check_settting_btn == True:
                    if back_setting_button.rect.collidepoint(x, y):
                        music.soundEffect(clicking = True)
                        menu_running = True
                        setting_running = False
                        check_settting_btn = False
                    if back_credits_button.rect.collidepoint(x, y):
                        music.soundEffect(clicking = True)
                        menu_running = True
                        credits_running = False
                        check_settting_btn = False
                     
menu()
