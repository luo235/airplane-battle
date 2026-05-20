import pygame
from .base_state import BaseState
from ui.button import Button
class GamePause(BaseState):
    def __init__(self, game_ctx):
        super().__init__(game_ctx)
        self.pause_button = Button(game_ctx.adapter.w_percent(30),game_ctx.adapter.h_percent(20),
        game_ctx.adapter.w_percent(40),game_ctx.adapter.h_percent(8),text="返回主菜单")
        self.pause_button.set_callbacks(on_click=lambda: game_ctx.change_state("menu")) 
    def enter(self):
        self.game_ctx.button.set_callbacks(on_click=self.game_ctx.resume)
        for anim in self.game_ctx.animations[:]:
            anim.pause()
    def exit(self):
        for anim in self.game_ctx.animations[:]:
            anim.resume()
    def handle_events(self,event):
        self.pause_button.handle_events(event)
        self.game_ctx.button.handle_events(event,100,100)
        
    def render(self):
        self.pause_button.draw(self.game_ctx.screen)
        self.game_ctx.button.set_text("")
        self.game_ctx.button.draw(self.game_ctx.button_surface)
        self.game_ctx.button.draw_polygen()
        self.game_ctx.screen.blit(self.game_ctx.button_surface,(100,100))
    