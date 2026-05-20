import pygame.font
class HUD:
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 72)
        #分数
        self.score = 0
        self.prep_score()
    def prep_score(self):
        score_str = f"{self.score:,}" 
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)
        self.score_image_rect = self.score_image.get_rect()
        self.score_image_rect.y = 80
        self.score_image_rect.x = self.screen_rect.right - 200
    def show_score(self):
        self.screen.blit(self.score_image, self.score_image_rect)