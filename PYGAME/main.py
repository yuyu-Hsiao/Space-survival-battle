from pickle import TRUE
from numpy import setbufsize
import pygame
import random
import os


FPS=60
WIDTH=500
HEIGHT=600

WHITE=(255,255,255)
GREEN=(0,255,0)
RED=(255,0,0)
BLACK=(0,0,0)
YELLOW=(255,255,0)




#遊戲初始化and創建視窗
pygame.init()
pygame.mixer.init()
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("GAME")
clock=pygame.time.Clock()


#載入圖片
player_img=pygame.image.load(os.path.join("img","player.png")).convert()
player_mini_img=pygame.transform.scale(player_img,(25,19))
player_mini_img.set_colorkey(BLACK)
bullet_img=pygame.image.load(os.path.join("img","bullet.png")).convert()
rock_imgs=[]
for i in range(7):
    rock_imgs.append(pygame.image.load(os.path.join("img",f"rock{i}.png")).convert())

expl_anim={}
expl_anim["lg"]=[]
expl_anim["sm"]=[]
expl_anim["player"]=[]
for i in range(9):
    expl_img=pygame.image.load(os.path.join("img",f"expl{i}.png")).convert()
    expl_img.set_colorkey(BLACK)
    expl_anim["lg"].append(pygame.transform.scale(expl_img,(75,75)))
    expl_anim["sm"].append(pygame.transform.scale(expl_img,(30,30)))
    
    player_expl_img=pygame.image.load(os.path.join("img",f"player_expl{i}.png")).convert()
    player_expl_img.set_colorkey(BLACK)
    expl_anim["player"].append(expl_img)

power_imgs={}
power_imgs["shield"]=pygame.image.load(os.path.join("img","shield.png")).convert()
power_imgs["gun"]=pygame.image.load(os.path.join("img","gun.png")).convert()





#載入音樂
shoot_sound=pygame.mixer.Sound(os.path.join("sound","shoot.wav"))
gun_sound=pygame.mixer.Sound(os.path.join("sound","pow1.wav"))
shield_sound=pygame.mixer.Sound(os.path.join("sound","pow0.wav"))
die_sound=pygame.mixer.Sound(os.path.join("sound","rumble.ogg"))
expls_sound=[
    pygame.mixer.Sound(os.path.join("sound","expl0.wav")),
    pygame.mixer.Sound(os.path.join("sound","expl1.wav"))
]
pygame.mixer.music.load(os.path.join("sound","background.ogg"))
pygame.mixer.music.set_volume(0.1)

font_name=os.path.join("TWKai.ttf")
#font_name=pygame.font.match_font("arial")
def draw_text(surf,text,size,x,y):
    font=pygame.font.Font(font_name,size)
    text_surface=font.render(text,True,WHITE)
    text_rect=text_surface.get_rect()
    text_rect.centerx=x
    text_rect.top=y
    surf.blit(text_surface,text_rect)

def new_rock():
    rock=ROCK()
    all_sprites.add(rock)
    rocks.add(rock)

def draw_health(surf,hp,x,y):
    if hp<=0:
        hp=0
    BAR_LENGHT=100
    BAR_HEIGHT=10
    fill=(hp/100)*BAR_LENGHT
    outline_rect=pygame.Rect(x,y,BAR_LENGHT,BAR_HEIGHT)
    fill_rect=pygame.Rect(x,y,fill,BAR_HEIGHT)
    pygame.draw.rect(surf,RED,fill_rect)
    pygame.draw.rect(surf,WHITE,outline_rect,2)

def draw_lives(surf,lives,img,x,y):
    for i in range(lives):
        img_rect=img.get_rect()
        img_rect.x=x+30*i
        img_rect.y=y
        surf.blit(img,img_rect)

#開始畫面
def draw_init():
    draw_text(screen,"太空生存戰!",64,WIDTH/2,HEIGHT/4)
    draw_text(screen,"按任意建開始遊戲",18,WIDTH/2,HEIGHT/2)
    pygame.display.update()
    waiting=True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:
                waiting=False
                return False


#結束畫面
def draw_end(score):
    draw_text(screen,"END",64,WIDTH/2,HEIGHT/4)
    draw_text(screen,"Your score is: %d"%(score),25,WIDTH/2,HEIGHT/2)
    draw_text(screen,"是否重新開始",20,WIDTH/2,HEIGHT*2/3-25)
    draw_text(screen,"是 : Y  否 : N",20,WIDTH/2,HEIGHT*2/3-50)
    pygame.display.update()
    waiting=True
    while waiting:
        clock.tick(FPS)
        key_pressd=pygame.key.get_pressed()
        for event in pygame.event.get():     
            if event.type == pygame.QUIT or key_pressd[pygame.K_n]:
                pygame.quit()
                return True
            elif key_pressd[pygame.K_y]:
                waiting=False
                return False
            


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(player_img,(60,50))
        self.image.set_colorkey(WHITE)
        self.rect=self.image.get_rect()  #定位圖片
        self.radius=25
        self.rect.centerx=WIDTH/2
        self.rect.bottom=HEIGHT-20
        self.speed=10
        self.health=100
        self.live=3
        self.hidden=False
        self.hidden_time=0
        self.gun=1
        self.gun_time=0


    def update(self):
        if self.gun>1 and pygame.time.get_ticks()-self.gun_time>5000:
            self.gun-=1
            self.gun_time=pygame.time.get_ticks()

        
        if self.hidden and pygame.time.get_ticks()-self.hidden_time>1000:
            self.rect.centerx=WIDTH/2
            self.rect.bottom=HEIGHT-20
            self.hidden=False

        key_pressd=pygame.key.get_pressed()
        if key_pressd[pygame.K_RIGHT] or key_pressd[pygame.K_d]:
            self.rect.x+=self.speed
        if key_pressd[pygame.K_LEFT] or key_pressd[pygame.K_a]:
            self.rect.x-=self.speed    
        if self.rect.right>WIDTH:
            self.rect.right=WIDTH
        if self.rect.left<0:
            self.rect.left=0

    def shoot(self):
        if self.hidden==False:
            if self.gun == 1:
                bullet=Bullet(self.rect.centerx,self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            elif self.gun>=2:
                bullet1=Bullet(self.rect.left,self.rect.centery)
                bullet2=Bullet(self.rect.right,self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()
               


    def hide(self):
        self.hidden=True
        self.hidden_time=pygame.time.get_ticks()
        self.rect.center=(WIDTH/2,HEIGHT+500)
    
    def gunup(self):
        self.gun+=1
        self.gun_time=pygame.time.get_ticks()



class ROCK(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_ori=random.choice(rock_imgs)
        self.image_ori.set_colorkey(BLACK)
        self.image=self.image_ori.copy()
        self.rect=self.image.get_rect()  #定位圖片
        self.radius=int(self.rect.width*0.85/2)
        self.rect.x=random.uniform(0,WIDTH-30)
        self.rect.y=random.uniform(-180,-240)
        self.speedy=random.uniform(2,10)
        self.speedx=random.uniform(-5,5)
        self.total_degree=0
        self.rot_degree=random.uniform(-5,5)

    def rotate(self):
        self.total_degree+=self.rot_degree
        self.total_degree=self.total_degree % 360
        self.image=pygame.transform.rotate(self.image_ori,self.total_degree)
        center=self.rect.center
        self.rect=self.image.get_rect()
        self.rect.center=center


    def update(self):
        self.rotate()   #處理石頭的旋轉
        self.rect.y+=self.speedy
        self.rect.x+=self.speedx
        if self.rect.top>HEIGHT or self.rect.left>WIDTH or self.rect.right<0:
            self.rect.x=random.uniform(0,WIDTH-30)
            self.rect.y=random.uniform(-100,-140)
            self.speedy=random.uniform(2,10)
            self.speedx=random.uniform(-3,3)

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.transform.scale(bullet_img,(15,33))
        self.image.set_colorkey(BLACK)
        self.rect=self.image.get_rect()  #定位圖片
        self.rect.centerx=x
        self.rect.bottom=y
        self.speedy=-25
       
    def update(self):
        self.rect.y+=self.speedy
        if self.rect.bottom<0:
            self.kill()
        
class Explosion(pygame.sprite.Sprite):
    def __init__(self,center,size):
        pygame.sprite.Sprite.__init__(self)
        self.size=size
        self.image=expl_anim[self.size][0]
        self.rect=self.image.get_rect()  #定位圖片
        self.rect.center=center
        self.frame=0
        self.last_updata = pygame.time.get_ticks()  #回傳初始化到現在經過的毫秒數
        self.frame_rate=40

       
    def update(self):
        now=pygame.time.get_ticks()
        if now-self.last_updata>self.frame_rate:
           self.last_updata=now
           self.frame+=1
           if self.frame ==len(expl_anim[self.size]):
               self.kill()
           else:
               self.image=expl_anim[self.size][self.frame] 
               center=self.rect.center
               self.rect=self.image.get_rect()
               self.rect.center=center

class Power(pygame.sprite.Sprite):
    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self)
        self.type=random.choice(["shield","gun"])
        self.image=power_imgs[self.type]
        self.image.set_colorkey(BLACK)
        self.rect=self.image.get_rect()  #定位圖片
        self.rect.center=center
        self.speedy=3

       
    def update(self):
        self.rect.y+=self.speedy
        if self.rect.top>HEIGHT:
            self.kill()


#遊戲暫停
flag = True
def game_stop():
    global flag
    flag = False
def game_go():
    global flag
    flag = True


all_sprites=pygame.sprite.Group()  #放spirte物件
rocks=pygame.sprite.Group()
bullets=pygame.sprite.Group()
power=pygame.sprite.Group()
player=Player()
all_sprites.add(player)
for i in range(8):
    new_rock()
score=0

pygame.mixer.music.play(-1)


#遊戲迴圈


show_init=True
running=True
while running:
    if show_init == True:
        close=draw_init()
        if close:
            break
        show_init = False
        all_sprites=pygame.sprite.Group()  #放spirte物件
        rocks=pygame.sprite.Group()
        bullets=pygame.sprite.Group()
        power=pygame.sprite.Group()
        player=Player()
        all_sprites.add(player)
        for i in range(8):
            new_rock()
        score=0
        

    clock.tick(FPS)     #一秒中最多更新FPS次
    #取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()



    #遊戲暫停
    key_pressd=pygame.key.get_pressed()
    if key_pressd[pygame.K_q]:  #q暫停
        game_stop()    
    while flag==False:
        draw_text(screen,"暫停",60,WIDTH/2,HEIGHT/2+10)
        pygame.display.update()
        for event in pygame.event.get():
            key_pressd=pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif key_pressd[pygame.K_w]:
                game_go()







    #更新遊戲
    all_sprites.update()
    hists=pygame.sprite.groupcollide(rocks,bullets,True,True)
    for hist in hists:
         random.choice(expls_sound).play()
         score+=hist.radius
         exp1=Explosion(hist.rect.center,"lg")
         all_sprites.add(exp1)
         new_rock()
         if random.random()>0.8:
             pow=Power(hist.rect.center)
             all_sprites.add(pow)
             power.add(pow)

    #判斷飛船跟石頭碰撞
    hits=pygame.sprite.spritecollide(player,rocks,TRUE,pygame.sprite.collide_circle)
    for hit in hits:
         new_rock()
         player.health-=hit.radius*0.7
         exp1=Explosion(hit.rect.center,"sm")
         all_sprites.add(exp1)
         if player.health<=0:
             die=Explosion(player.rect.center,"player")
             all_sprites.add(die)
             die_sound.play()
             player.live-=1
             player.health=100
             player.hide()
    
    #判斷寶物跟飛船碰撞         
    hits=pygame.sprite.spritecollide(player,power,TRUE)    
    for hit in hits:
         if hit.type == "shield":
             shield_sound.play()
             player.health+=20
             if player.health>100:
                 player.health=100
         elif hit.type == "gun":
             player.gunup()
             gun_sound.play()




    #命用完後
    if player.live == 0 and not(die.alive()):
            close=draw_end(score) 
            if close:
                break
            all_sprites=pygame.sprite.Group()  #放spirte物件
            rocks=pygame.sprite.Group()
            bullets=pygame.sprite.Group()
            power=pygame.sprite.Group()
            player=Player()
            all_sprites.add(player)
            for i in range(8):
                new_rock()
            score=0
            
 
        
    #畫面顯示
    screen.fill(BLACK)
    all_sprites.draw(screen)
    draw_text(screen,str(score),18,WIDTH/2,10)
    draw_health(screen,player.health,5,15)
    draw_lives(screen,player.live,player_mini_img,WIDTH-100,15)
    pygame.display.update()



pygame.quit()

