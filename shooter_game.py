#Создай собственный Шутер!

from pygame import *
from random import *     
from time import time as timer



mixer.init()
mixer.music.load('Space1.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

img_hero = 'rocket.png'
img_back = 'tgalaxy.jpg'
img_enemy = 'ufo.png'
img_bullet = 'bullet.png'
img_ast = "asteroid.png"

lost = 0
score = 0
max_lost = 1

font.init()
font1 = font.SysFont('Arial', 36)
win = font1.render('С вас 100 рублей за игру иначе в ваш дом приедет ОМОН за кражу 100 миллионов долларов', True, (0, 255,0))
lose = font1.render('С вас 10000 рублей', True, (255, 0,0))
tsel = 1000 
class GameSprite(sprite.Sprite):
   #конструктор класса
    def __init__(self, player_image, player_x, player_y,size_x, size_y, player_speed):
        super().__init__()
    # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y


    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


#класс-наследник для спрайта-игрока (управляется стрелками)
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15,20,-40)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
class Enemy1(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


#класс-наследник для спрайта-врага (перемещается сам)


win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption('Shooter Cyberpunk 2077 alien invasion forza horizon 2077 insane mode')
background = transform.scale(image.load(img_back), (win_width, win_height))

bullets = sprite.Group()
player = Player(img_hero, 300, 400, 50, 80, 15)
player1 = Player(img_hero, 200, 400, 50, 80, 15)
player2 = Player(img_hero, 400, 400, 50, 80, 15)

monsters = sprite.Group()
for i in range (1,40):
    rspeed = randint(1, 2)
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 30, 50, rspeed)
    monsters.add(monster)
asteroids = sprite.Group()
asteroidSpeed = randint(4,5)
for i in range(1,3):
    asteroid = Enemy1(img_ast, randint(30, win_width - 30), -40, 80, 50,asteroidSpeed)
    asteroids.add(asteroid)
#! Лето жаркое очень Да ладно
finish = False
run = True
reload = False 
num_fire = 0

while run:
    for knopka in event.get():
        if knopka.type == QUIT:
            run = False
        if knopka.type == KEYDOWN:
            if knopka.key == K_SPACE:
                if num_fire < 100 and reload == False:
                    fire_sound.play()
                    player.fire()
                    player1.fire()
                    player2.fire()
                    num_fire += 3
                if num_fire >= 100 and reload == False:
                    shoot_time = timer()
                    reload = True
    if not finish:
        window.blit(background, (0,0))
        text = font1.render('Счёт: ' + str(score), 1, (255, 255, 255))
        text1 = font1.render('Цель: ' + str(tsel), 1, (00, 255, 255))
        window.blit(text, (10,20))
        window.blit(text1, (10,80))
        text_lose = font1.render('Пролетели: ' + str(lost), 1, (255, 255,255))
        window.blit(text_lose, (10, 50))
        player1.update()
        player.update()
        player2.update()
        asteroids.update()
        monsters.update()
        bullets.update()
        player1.reset()
        player2.reset()
        player.reset()
        monsters.draw(window)
        asteroids.draw(window)
        bullets.draw(window)
        #! Кто сказал что это мой код?
        if reload == True:
            now_time = timer()
            if now_time - shoot_time <2:
                reload1 = font1.render('Перезарядка...',1,(150,0,0))
                window.blit(reload1,(260, 460))
                print(reload)
            else:
                print(reload)
                num_fire = 0
                reload = False
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 30, 50, rspeed)
            monsters.add(monster)
        if sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player, asteroids, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (250,200))
        if score >= tsel:
            finish = True
            window.blit(win, (250,200))
        display.update()

    time.delay(50)

    #ПЛОХАЯ ИГРА ОБНОВ НЕТУ, РАЗРАБОТЧИКИ ЗАЖРАЛИСЬ