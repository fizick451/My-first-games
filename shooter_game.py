from pygame import *
from pygame import Surface
from random import *
from time import time as timer
#создай окно игры
win_height = 500
win_width = 700

win = display.set_mode((win_width, win_height))

display.set_caption('шутер')

bg = transform.scale(image.load("galaxy.jpg"),(700, 500))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

score = 0
lost = 0
font.init()
font1 = font.SysFont('Arial',25)
text_lose = font1.render(
    "Пропущено: " + str(lost), 1, (255, 255, 255)
    )
text_win = font1.render(
    "Сбито: " + str(score), 1, (255, 255, 255)
    )

class GameSprite(sprite.Sprite):
        def __init__(self, player_image, player_x, player_y,size1,size2, player_speed):
                super().__init__()
                
                self.image = transform.scale(image.load(player_image),(size1, size2))
                self.speed = player_speed
                self.rect = self.image.get_rect()
                self.rect.x = player_x
                self.rect.y = player_y
        def reset(self):
                win.blit(self.image,(self.rect.x, self.rect.y))
        


class Player(GameSprite):
        def update(self):
                keys = key.get_pressed()
                if keys[K_LEFT] and self.rect.x > 5:
                        self.rect.x -= self.speed
                if keys[K_RIGHT] and self.rect.x < win_width - 80:
                        self.rect.x += self.speed
        def fire(self):
                button = Button("bullet.png",self.rect.centerx - 20, self.rect.top,40,30, 15)
                buttons.add(button)
class Enemy(GameSprite):
        def update (self):
                self.rect.y += self.speed
                global lost
                if self.rect.y == 500:
                        self.rect.y = 0
                        self.rect.x = randint(20,680)
                        lost += 1

class Button(GameSprite):
        def update(self):
                self.rect.y -= self.speed
                if self.rect.y < 0:
                        self.kill()

#------
rocket = Player('rocket.png', 300, 400,100,80, 4)
#------
monstrs = sprite.Group()
monster1 = Enemy('ufo.png', 50, 20,60,60, randint(1,2))
monster2 = Enemy('ufo.png', 100, 40,60,60, randint(1,2))
monster3 = Enemy('ufo.png', 125, 30,60,60, randint(1,2))
monster4 = Enemy('ufo.png', 180, 50,60,60, randint(1,2))
monster5 = Enemy('ufo.png', 420, 21,60,60, randint(1,2))
monstrs.add(monster1)
monstrs.add(monster2)
monstrs.add(monster3)
monstrs.add(monster4)
monstrs.add(monster5)
#-----
buttons = sprite.Group()
#----
asteroid1 = Enemy('asteroid.png', 50, 20,60,60, 1)
asteroid2 = Enemy('asteroid.png', 145, 71,75,60, 2)
asteroids = sprite.Group()
asteroids.add(asteroid1)
asteroids.add(asteroid2)

clock = time.Clock()
FPS = 50       

num_fire = 0
rel_time = False

finish = False
game = True
while game:
        
        for e in event.get():
                
                if e.type == QUIT:

                        game = False 
                #---------------------
                elif e.type == KEYDOWN:
                        if e.key == K_SPACE:
                                if num_fire < 5 and rel_time == False:
                                        rocket.fire()
                                        num_fire += 1
                                if num_fire == 5 and rel_time == False:
                                        last_time = timer()
                                        rel_time = True
        
        if finish != True:

                win.blit(bg,(0,0))
                text_lose = font1.render("Пропущено: " + str(lost), 1, (255, 255, 255))
                text_win = font1.render("сбито: " + str(score), 1, (255, 255, 255))
                win.blit(text_lose,(20,20))
                win.blit(text_win,(20,50))
                #-----
                rocket.reset()                
                rocket.update()    
                #-----
                monstrs.draw(win)
                monstrs.update()
                #----
                buttons.draw(win)
                buttons.update() 
                #------
                asteroids.draw(win)
                asteroids.update()
                #столкновения--------
                if sprite.groupcollide(monstrs,buttons,True,True):
                        score = score + 1
                        monster = Enemy('ufo.png', randint(20,680), 20,60,60, 2)
                        monstrs.add(monster)
                if sprite.spritecollide(rocket,monstrs,False):
                        win.blit(bg,(0,0))
                        finish = True
                        aaa = font1.render('YOU LOSE', 1,  (150,0,0))
                        win.blit(aaa, (450,400))
                
                if sprite.spritecollide(rocket,asteroids,False):
                        win.blit(bg,(0,0))
                        finish = True
                        aaa = font1.render('YOU LOSE', 1,  (150,0,0))
                        win.blit(aaa, (250,460))
                
                
                
                if score == 10:
                        win.blit(bg,(0,0))
                        finish = True
                        www = font1.render('YOU WIN', 1,  (150,0,0))
                        win.blit(www, (250,460))
                
                if lost == 3:
                        win.blit(bg,(0,0))
                        finish = True
                        aaa = font1.render('YOU LOSE', 1,  (150,0,0))
                        win.blit(aaa, (450,250))
                if rel_time == True:
                        now_time = timer()

                        if now_time - last_time < 1:
                                reload = font1.render('wait, reload....', 1,  (150,0,0))
                                win.blit(reload, (260,460))
                        else:
                                num_fire = 0
                                rel_time = False


        
        
        
        
        display.update()
        clock.tick(FPS)
        #https://docs.google.com/presentation/d/1oLE7e_XGBZB97VBz6wjMD5w_qDp8B2-xw3-RZNzmXXI/edit#slide=id.gbf206be851_0_0
