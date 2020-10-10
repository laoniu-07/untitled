import pygame
from   pygame.locals import *
from pygame.math import Vector2
import random
SCREEN_SIZE=(800, 500)
W,H=SCREEN_SIZE
class state():
    def __init__(self,name):
        self.name=name

class AntExploring(state):
    def __init__(self,ant):
        state.__init__(self,'exploring')
        self.ant=ant
        self.leaf_id=None
    def radom_destination(self):
        self.ant.destination=Vector2(random.randint(0,SCREEN_SIZE[0]),random.randint(0,SCREEN_SIZE[1]))
    def entry_active(self):
        self.ant.speed=120+random.randint(-30,30)
        self.radom_destination()


class StateMachine():
    def __init__(self):
        self.states = {}
        self.action_state = None
    def add_state(self,state):
        self.states[state.name]=state
    def set_state(self,name):
        if self.states[name] is not None:
            return
        self.action_state = self.states[name]
        self.action_state.entry_active()
class Word():
    def __init__(self):
        self.entitys={}
        self.id=1
    def add(self,entity):
        self.entitys[self.id]=entity
        self.id+=1
    def render(self,screen):
        for entity  in list(self.entitys.values()):
            entity.render(screen)
    def process(self):

        for i in self.entitys:
            i.process()
class GameEntity():
    def __init__(self,name,image,word):
        self.destination=0
        self.speed=0
        self.name=name
        self.word=word
        self.image = image
        self.brain=StateMachine()
        self.image_size = self.image.get_size()
        self.rect = (random.randint(0, W - self.image_size[0]), random.randint(0, H - self.image_size[1]), *self.image_size)
    def render(self,screen):
        screen.blit(self.image,self.rect)

class Ant(GameEntity):
    def __init__(self,image,word):
        GameEntity.__init__(self,'ant',image,word)
        exloring_state=AntExploring(self)
        self.brain.add_state(exloring_state)
def run():
    pygame.init()
    screen = pygame.display.set_mode((800, 500))
    screen.fill((255,255,255))
    clock = pygame.time.Clock()
    ant_image = pygame.image.load("ant.png")   #.convert_alpha()
    word=Word()
    a = Ant(ant_image,word)
    s.set_state('exploring')
    word.add(a)

    while 1:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type==QUIT:
                exit()

        screen.fill((255, 255, 255))
        word.process()
        word.render(screen)
        pygame.display.update()

if __name__=='__main__':
    run()