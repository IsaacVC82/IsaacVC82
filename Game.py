import pygame
import sys 
import random 
pygame.init()
pygame.mixer.init()
WIDTH = 800 
HEIGHT = 600
BLACK=(0,0,0)
WHITE=(255,255,255)
screen=pygame.display.set_mode(size = (800, 600))
#Aqui va el titulo de la ventana 
pygame.display.set_caption("Shooter!")
#Aqui programamos el reloj
clock=pygame.time.Clock()


def draw_text(surface, text , size, x, y):
    font = pygame.font.SysFont("serif",size)
    text_surface= font.render(text, True, WHITE)
    text_rect= text_surface.get_rect()
    text_rect.midtop= (x,y)
    surface.blit(text_surface, text_rect)
def draw_sheild_bar(surface, x, y, percentage):
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = ( percentage/100)* BAR_LENGTH
    border = pygame.Rect(x,y,BAR_LENGTH, BAR_HEIGHT)
    fill = pygame.Rect(x,y,fill, BAR_HEIGHT) 
    pygame.draw.rect(surface, WHITE,fill) 
    pygame.draw.rect(surface, BLACK,border, 3  )  

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/player.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx=400
        self.rect.bottom=550
        self.speed_x = 0
        self.shield = 100

    def update(self):
        self.speed_x= 0
        keystate=pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x=-5
        if keystate[pygame.K_RIGHT]:
            self.speed_x=5
        self.rect.x += self.speed_x
        if self.rect.right > 800:
            self.rect.right = 800
        if self.rect.left < 0:
            self.rect.left = 0  
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        #  laser_sound.play()           
        
class Meteor (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(meteor_images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH -self.rect.width)
        self.rect.y = random.randrange(-140, -100)
        self.speedy = random.randrange(1,10)
        self.speedx = random.randrange(-5, 5)

    def update(self):
        self.rect.y +=self.speedy
        self.rect.x +=self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -40 or self.rect.right > WIDTH + 40:
            self.rect.x = random.randrange(WIDTH -self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1,10)
class Bullet(pygame.sprite.Sprite):
    def __init__ (self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/laser1.png")
        self.image.set_colorkey(BLACK) 
        self.rect = self.image.get_rect()
        self.rect.y = y 
        self.rect.centerx = x 
        self.speedy= -10 
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
           self.kill()  
class Explosion(pygame.sprite.Sprite):
     def __init__(self, center):
         super().__init__()
         self.image = explosion_anim[0] 
         self.rect= self.image.get_rect()
         self.rect.center = center
         self.frame = 0
         self. last_update = pygame.time.get_ticks() 
         self.frame_rate = 50 #velocidad de explosion 

     def update(self):
        now = pygame.time.get_ticks()
        if now -self.last_update> self.frame_rate:
            self.last_update = now 
            self.frame += 1
        if self.frame == len(explosion_anim):
            self.kill() 
        else:
            center = self.rect.center
            self.image = explosion_anim[self.frame] 
            self.rect = self.image.get_rect()
            self.rect.center = center    
def show_go_screen():
    screen.blit(background, [0,0])
    draw_text(screen, "SHOOTER!", 65, WIDTH//2,HEIGHT//4)
    draw_text(screen,"Press Key", 27, WIDTH//2 , HEIGHT//2)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False    
meteor_images= []            
meteor_list= ["assets/meteor1.png", "assets/meteor2.png", "assets/meteor3.png", "assets/meteor4.png", "assets/meteor5.png"]
for img in meteor_list:
    meteor_images.append(pygame.image.load(img).convert())

#------Animacion explosiones meteoro 
explosion_anim= []
for i in range (9):
    file = "assets/regularExplosion0{}.png".format(i)
    img = pygame.image.load(file).convert()
    img.set_colorkey(BLACK)
    img_scale = pygame.transform.scale(img, (70,70)) 
    explosion_anim.append(img_scale)   

#Cargar imagen de fondo
background = pygame.image.load("assets/background.png").convert() 
#Cargar sonidos
#laser_sound = pygame.mixer.Sound("assets/assets_laser5(1).ogg")
explosion_sound=pygame.mixer.Sound("assets/assets_explosion.wav")
#pygame.mixer.music.load("assets/music.ogg")
#pygame.mixer.music.set_volume(.2)

#sprites           

#    pygame.mixer.music.play()  
#----Pantalla Game Over   
game_over = True
#Loop principal 
running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        meteor_list = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range (6):
            meteor = Meteor()
            all_sprites.add(meteor)
            meteor_list.add(meteor)
        score = 0     

    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: 
                player.shoot()

    all_sprites.update()

    #colisiones metoro - laser
    hits = pygame.sprite.groupcollide(meteor_list, bullets, True, True)
    for hit in hits:
        score += 100
        explosion = Explosion(hit.rect.center)
        all_sprites.add(explosion)
        explosion_sound.play()
        meteor= Meteor()
        all_sprites.add(meteor)
        meteor_list.add(meteor)
 



    #Detectar colisiones jugador - meteoro
    hits = pygame.sprite.spritecollide(player, meteor_list, True)
    for hit in  hits:
        player.shield -= 20 
        meteor= Meteor()
        all_sprites.add(meteor)
        meteor_list.add(meteor)
        if player.shield <= 0:
            game_over = True 
    
    screen.blit(background, [0,0])

    all_sprites.draw(screen)

    #Marcador
    draw_text(screen, str(score), 30, WIDTH//2, 10)
    #Salud 
    draw_sheild_bar(screen, 5, 5, player.shield)
    pygame.display.flip()
pygame.quit()           
