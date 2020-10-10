import pygame,time
from pygame.math import *
from pygame.locals import *
import  random

pygame.init()
screen=pygame.display.set_mode((600,500))
#bg=pygame.Surface((600,500),flags=SRCALPHA)
bg_suface = pygame.Surface((600,500), flags=pygame.SRCALPHA)
pygame.Surface.convert(bg_suface)
bg_suface.fill(pygame.Color(0, 0, 0, 16))
screen.fill((0, 0, 0))
clock=pygame.time.Clock()
class RainCode(pygame.sprite.Sprite):
    def __init__(self,time_pass):
        pygame.sprite.Sprite.__init__(self)
        text_sprite=pygame.font.SysFont(self.get_font(),20).render(self.get_text(),True,self.get_color())
        text_sprite_rotate=pygame.transform.rotate(text_sprite,90)
        self.speed=random.randint(100,200)
        self.time_pass=time_pass
        self.image=text_sprite_rotate
        self.rect=self.image.get_rect()
        self.rect.left=random.randint(0,600)

    def get_text(self):
        text=''
        for i in range(random.randint(5,10)):
            text+=str(random.choice((0,1)))
        print(text)
        return text
    def get_font(self):
        fonts = pygame.font.get_fonts()

        return fonts[2]
    def get_color(self):
        color=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
        return color
    def update(self):
        self.rect.y+=self.speed*time_pass
        print(self.rect)
        if self.rect.y>500 or random.randint(1,8)==1:
            self.kill()

sprintes=pygame.sprite.Group()
while 1:
    for event in pygame.event.get():
        if event.type==QUIT:
            exit()
    time_pass=clock.tick(10)/1000

    s=RainCode(time_pass)
    sprintes.add(s)


    screen.blit(bg_suface,(0,0))
    sprintes.update()
    sprintes.draw(screen)

    pygame.display.update()