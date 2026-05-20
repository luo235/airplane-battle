import pygame
from settings import Settings

class Airplane:
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.ai_game=ai_game
        # 飞机图片（正常、左倾、右倾）
        self.image_normal = pygame.image.load('resource/images/airplane.bmp')
        self.image_normal = pygame.transform.smoothscale(self.image_normal, (80, 100))
        self.image_left = pygame.transform.rotate(self.image_normal, 10)
        self.image_left = pygame.transform.smoothscale(self.image_left, (80, 100))
        self.image_right = pygame.transform.rotate(self.image_normal, -10)
        self.image_right = pygame.transform.smoothscale(self.image_right, (80, 100))

        self.image = self.image_normal
        self.rect = self.image_normal.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.y-=20
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        # 移动开关
        self.moving_right = False
        self.moving_left = False
        self.moving_top = False
        self.moving_bottom = False
        # 血条
        self.bar_width = 10
        self.max_hp = self.settings.airplane_max_hp
        self.hp = self.max_hp
        self.bar_lenth = self.max_hp / 2
        # 经验条
        self.xp_bar_lenth = 80
        self.xp_bar_width = 10
        self.xp = 100
        self.max_xp = 100
        # 属性
        self.speed = self.settings.airplane_speed
        self.hp_heal = 0.01
        
    def draw_xp(self):
        self.empty_xp = int((self.max_xp - self.xp) / self.max_xp * self.xp_bar_lenth)
        self.fill_xp = self.xp_bar_lenth - self.empty_xp
        xp_rect_x = self.rect.x
        xp_rect_y = self.rect.bottom + 20
        pygame.draw.rect(self.screen, (60, 60, 60), 
                         (xp_rect_x, xp_rect_y, self.xp_bar_lenth, self.xp_bar_width))
        pygame.draw.rect(self.screen, (30, 200, 30), 
                         (xp_rect_x, xp_rect_y, self.fill_xp, self.xp_bar_width))

    def blit_airplane(self):
        self.screen.blit(self.image, self.rect)

    def draw_hp(self):
        self.bar_lenth = self.max_hp / 2
        self.empty_bar = int((self.max_hp - self.hp) / self.max_hp * self.bar_lenth)
        self.fill_bar = self.bar_lenth - self.empty_bar
        hp_rect_x = self.rect.x
        hp_rect_y = self.rect.bottom + 10
        pygame.draw.rect(self.screen, (60, 60, 60), 
                         (hp_rect_x, hp_rect_y, self.bar_lenth, self.bar_width))
        pygame.draw.rect(self.screen, (200, 30, 30), 
                         (hp_rect_x, hp_rect_y, self.fill_bar, self.bar_width))

    def _update_airplane(self):
        self.image = self.image_normal
        if self.moving_left and self.rect.x >= 0:
            self.image = self.image_left
            self.x -= self.speed
        if self.moving_right and self.rect.right <= self.screen_rect.right:
            self.image = self.image_right
            self.x += self.speed
        if self.moving_bottom and self.rect.bottom <= self.screen_rect.bottom:
            self.y += self.speed
        if self.moving_top and self.rect.y >= 0:
            self.y -= self.speed
        self.rect.x = self.x
        self.rect.y = self.y
        if self.hp < self.max_hp:
            self.hp += self.hp_heal

    def joystick_update_airplane(self,dx,dy,r): 
        self.x+=self.speed*(dx/r)
        self.y+=self.speed*(dy/r)
        if self.x <= 0:
            self.x = 0
        elif self.x + self.rect.width > self.screen_rect.right:
             self.x = self.screen_rect.right - self.rect.width
        if self.y <= 0:
            self.y=0
        elif self.y + self.rect.height > self.screen_rect.bottom:
             self.y = self.screen_rect.bottom - self.rect.height
        self.rect.y = self.y
        self.rect.x = self.x
        if self.hp < self.max_hp:
            self.hp += self.hp_heal