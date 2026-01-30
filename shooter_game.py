from pygame import*
from random import randint
from time import time as timer
jendela = display.set_mode((700, 500))
display.set_caption('pygame window')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
jam = time.Clock()
fire_sound = mixer.Sound('fire.ogg')

class gamesprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image,), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        jendela.blit(self.image, (self.rect.x, self.rect.y))

class player(gamesprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 700 - 80:
            self.rect.x += self.speed
    def fire(self):
        amunisi = bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 50, 15)
        peluru.add(amunisi)
        
lose = 0
class enemy(gamesprite):
    def update(self):
        self.rect.y += self.speed
        global lose
        if self.rect.y > 440:
            self.rect.y = 0
            self.rect.x = randint(80, 640)
            lose += 1

class bullet(gamesprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


            


        

font.init()
font1 = font.SysFont('Arial', 30)
font2 = font.SysFont('arial', 100)
font3 = font.SysFont('Arial', 50)
num_fire = 0
reload = False
peluru = sprite.Group()
ufo = sprite.Group()
meteor = sprite.Group()
for i in range (1, 3):
    asteroid = enemy('asteroid.png', randint(80, 700-80), -40, 80, 50, randint(1, 2))
    meteor.add(asteroid)
for i in range(1, 6):
    UFO = enemy('ufo.png', randint(80, 700 - 80), -40, 80, 50, randint(1, 2))
    ufo.add(UFO)
pemain = player('rocket.png', 300, 400, 80, 100, 5)
finish = False
game = True
menang = font2.render('you win', 1, (255, 0, 0))
kalah = font2.render('you lose', 1, (255, 0, 0))
poin = 0
while game:
    

    for i in event.get():
        if i.type == QUIT:
            game = False
        elif i.type == KEYDOWN:
            if i.key == K_SPACE:
                if num_fire < 10 and reload == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    pemain.fire()
                if num_fire >= 10 and reload == False:
                    last_time = timer()
                    reload = True
            
        
                
    if not finish:
        jendela.blit(background, (0, 0))
        pemain.reset()
        pemain.update()
        ufo.update()
        ufo.draw(jendela)
        peluru.update()
        peluru.draw(jendela)
        skor = font1.render('skor '+ str(poin),1,(255, 255, 255))
        missed = font1.render('missed '+ str(lose), 1, (255, 255, 255))
        jendela.blit(skor,(20, 20))
        jendela.blit(missed,(20, 40))
        meteor.update()
        meteor.draw(jendela)
        if sprite.spritecollide(pemain, ufo, False) or lose >= 5 or sprite.spritecollide(pemain, meteor, False):
            finish = True
            jendela.blit(kalah, (200, 200))
        
        tabrak = sprite.groupcollide(ufo, peluru, True, True)
        tabrak1 = sprite.groupcollide(meteor, peluru, True, True)
        for i in tabrak1:
            poin += 1 
            asteroid = enemy('asteroid.png', randint(80, 700-80), -40, 80, 50, randint(1, 5))
            meteor.add(asteroid)

        for i in tabrak:
            poin += 1
            musuh = enemy('ufo.png', randint(80, 700 - 80), -40, 80, 50, randint(1, 5) )
            ufo.add(musuh)
        if reload:
            now_time = timer()
            if now_time - last_time < 3:
                reloader = font3.render('reloading..', 1,(150, 0, 0))
                jendela.blit(reloader, (260, 460))
            else:
                num_fire = 0
                reload = False
    jam.tick(60)    

    display.update()
display.update()
