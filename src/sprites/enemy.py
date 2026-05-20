import pygame
import random
from pygame.sprite import Sprite
class Enemy(Sprite):
    def __init__(self,ai_game):
        super().__init__()
        self.screen=ai_game.screen
        self.screen_rect=ai_game.screen.get_rect()
        self.settings=ai_game.settings
        self.enemy_image=pygame.image.load('resource/images/enemy.bmp')
        self.enemy_image=pygame.transform.smoothscale(self.enemy_image,(80,100))
        self.rect=self.enemy_image.get_rect()
        self.rect.x=random.randint(0,self.screen_rect.width-self.rect.width)
        self.rect.y=random.randint(-100,-20)
        self.y = float(self.rect.y)
        self.bar_lenth=80
        self.bar_width=10
        self.hp=20
        self.max_hp=20
        self.speed=self.settings.enemy_speed
        
    def draw_hp(self) :
        self.empty_bar=int((self.max_hp-self.hp)/self.max_hp*self.bar_lenth)
        self.fill_bar=self.bar_lenth-self.empty_bar
        hp_rect_x=self.rect.x
        hp_rect_y=self.rect.top-10
        pygame.draw.rect(self.screen,(60,60,60),(hp_rect_x,hp_rect_y,self.bar_lenth,self.bar_width))
        pygame.draw.rect(self.screen,(200,30,30),(hp_rect_x,hp_rect_y,self.fill_bar,self.bar_width))    
    def blit_enemy(self):
        self.screen.blit(self.enemy_image,self.rect)   
    def update(self):
        self.y+=self.speed
        self.rect.y=self.y  