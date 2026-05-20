import pygame
from pygame.sprite import Sprite 


class EnemyBullet(Sprite):
    def __init__(self, ai_game, enemy):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.bullet_color = self.settings.enemy_bullet_color
        self.rect = pygame.Rect(0,0,self.settings.enemy_bullet_width,self.settings.enemy_bullet_height )
        self.rect.midbottom = enemy.rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.atk = self.settings.enemy_bullet_atk
        self.speed = self.settings.enemy_bullet_speed
        self.speed_x = 0

    def update(self):
        self.atk = self.settings.enemy_bullet_atk
        self.x += self.speed_x
        self.y += self.speed
        self.rect.x = self.x
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.bullet_color, self.rect)