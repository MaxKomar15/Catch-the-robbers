from typing import Any
from pygame import *
from random import randint
from pygame import *
init()
mixer.init()
font.init()

FPS = 60
screen_info = display.Info()
WIDTH, HEIGHT = screen_info.current_w, screen_info.current_h
flags = FULLSCREEN
window = display.set_mode((WIDTH, HEIGHT), flags)

font1 = font.SysFont("Arial", 40)
font2 = font.SysFont("Arial", 65)

# mixer.music.load("space.ogg") 
# mixer.music.set_volume(0.2)
# mixer.music.play(loops=-1)

window = display.set_mode((WIDTH, HEIGHT)) #створюємо вікно 
display.set_caption("Cath the robbers")
clock = time.Clock() # Створюємо ігровий таймер

bg = image.load("images/road-texture4.png") # завантажуємо картинку в гру
bg = transform.scale(bg, (WIDTH, HEIGHT)) #змінюємо розмір картинки
player_img = image.load('images/Police.png')
player_images = [
    transform.scale(image.load('images/Police_animation/1.png'), (300, 300)),  
     transform.scale(image.load('images/Police_animation/2.png'), (300, 300)),  
      transform.scale(image.load('images/Police_animation/3.png'), (300, 300)),  
    
]

enemy_img = image.load('images/Black_viper.png')
NPC_img = image.load('images/Car.png')
bg_y1 = 0
bg_y2 = -HEIGHT


sprites = sprite.Group()

class GameSprite(sprite.Sprite):
    def __init__(self, sprite_image, width, height, x, y):
        super().__init__()
        self.image = transform.scale(sprite_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = mask.from_surface(self.image)
        sprites.add(self)

    def draw(self, window):
        window.blit(self.image, self.rect)

class Player(GameSprite):
    def __init__(self, sprite_image, width, height, x, y):
        super().__init__(sprite_image, width, height, x, y)
        self.images = player_images
        self.index = 0
        self.frame = 0
        self.max_frame = 20

        self.start_rect = self.rect
        self.hp = 100
        self.points = 0
        self.speed = 5
        self.bg_speed = 0
        self.max_speed = 20

    def update(self):
        global hp_text
        self.old_pos = self.rect.x, self.rect.y

        keys = key.get_pressed() #отримуємо список натиснутих клавіш
        if keys[K_w]:
            if self.rect.y > 350:
                self.rect.y -= self.speed
            if self.bg_speed < self.max_speed:
                self.bg_speed += 0.2 
        elif keys[K_s] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
            self.bg_speed = 1
        else:
            if self.bg_speed >= 2:
                self.bg_speed -= 0.2


        if keys[K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.right < WIDTH:
            self.rect.x += self.speed

        self.frame += 1
        if self.frame >= self.max_frame:
            self.frame = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            
            self.image = self.images[self.index]


NPC_Group = sprite.Group()

class NPC(GameSprite):
        def __init__(self):
            rand_x = randint(50, WIDTH-350)
            y = -500
            super().__init__(NPC_img, 300, 300, rand_x, y)
            self.speed = -5
            if not sprite.spritecollide(self, NPC_Group, False):
                NPC_Group.add(self)
            else:
                self.kill()


        def update(self):
            global points_text
            self.rect.y += self.speed + player.bg_speed
            if self.rect.y > HEIGHT:
                self.kill()
                player.points += 10
                points_text = font1.render(F"Points: {player.points}", True, (255, 255, 255))
            
class Robber(GameSprite):
        def __init__(self):
            rand_x = randint(0, WIDTH-70)
            y = 200
            super().__init__(enemy_img, 300, 300, rand_x, y)
            self.speed = 10
           
        def update(self):
            self.rect.y -= self.speed
            if self.rect.bottom < 0:
                self.speed = 0

player = Player(player_img, 300, 300, WIDTH/2, HEIGHT-400)
robber = Robber()

hp_text = font1.render(F"HP: {player.hp}", True, (255, 255, 255))
points_text = font1.render(F"Points: {player.points}", True, (255, 255, 255))
finish_text = font2.render("[>GAME OVER<]", True, (255, 0, 0))

finish = False
stop_spawn = False
last_spawn_time = time.get_ticks()
spawn_interval = randint(3000, 5000)

while True:
    #оброби подію «клік за кнопкою "Закрити вікно"
    for e in event.get():
        if e.type == QUIT:
            quit()
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                quit()

    if not finish:
        now = time.get_ticks()
        if now - last_spawn_time > spawn_interval:
            if len(NPC_Group) < 10:
                NPC()
            last_spawn_time = time.get_ticks()
            spawn_interval = randint(1000, 3000)
        collide_list = sprite.spritecollide(player, NPC_Group, False, sprite.collide_mask)
        for enemy in collide_list:
            player.hp -= 25
            hp_text = font1.render(F"HP: {player.hp}", True, (255, 255, 255))
            NPC_Group.remove(enemy)

        sprites.update()
      
        if player.hp <= 0:
            finish = True

        if player.points >= 200:
            stop_spawn = True

        if stop_spawn and not finish:
            robber.speed = -5
            if player.rect.y < robber.rect.y:
                finish = True
                finish_text = font2.render("[>You Win<]", True, (0, 255, 0))

        

        

        window.blit(bg, (0,bg_y1))
        window.blit(bg, (0,bg_y2))
        bg_y1 += player.bg_speed
        bg_y2 += player.bg_speed
        if bg_y1 > HEIGHT:
            bg_y1 = -HEIGHT
        if bg_y2 > HEIGHT:
            bg_y2 = -HEIGHT
    sprites.draw(window)
    window.blit(hp_text, (10, 10))
    window.blit(points_text, (WIDTH-200, 10))
    if finish:
        window.blit(finish_text, (WIDTH/2 - 150,  HEIGHT/2))
    display.update()
    clock.tick(FPS)