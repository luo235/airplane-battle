import pygame
from pygame.sprite import Sprite

class Boss(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.image = pygame.image.load("resource/images/enemy.bmp")
        self.image = pygame.transform.smoothscale(self.image, (180, 180))
        self.rect = self.image.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.y = 60
        self.x = float(self.rect.x)
        self.speed = self.settings.boss_speed
        self.direction = 1
        self.hp = self.settings.boss_hp
        self.max_hp = self.settings.boss_max_hp
        self.bar_lenth = self.rect.width
        self.bar_width = 15

    def update(self):
        self.x += self.speed * self.direction
        if self.x <= 0:
            self.x = 0
            self.direction = 1
        elif self.x + self.rect.width >= self.screen_rect.right:
            self.x = self.screen_rect.right - self.rect.width
            self.direction = -1
        self.rect.x = self.x

    def blit_boss(self):
        self.screen.blit(self.image, self.rect)

    def draw_hp(self):
        self.empty_bar = int((self.max_hp - self.hp) / self.max_hp * self.bar_lenth)
        self.fill_bar = self.bar_lenth - self.empty_bar
        hp_rect_x = self.rect.x
        hp_rect_y = self.rect.top - 20
        pygame.draw.rect(
        self.screen,
        (60, 60, 60),
        (hp_rect_x, hp_rect_y, self.bar_lenth, self.bar_width)
         )
        pygame.draw.rect(
        self.screen,
        (200, 30, 30),
        (hp_rect_x, hp_rect_y, self.fill_bar, self.bar_width)
         )