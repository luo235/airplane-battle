import pygame
from .base_state import BaseState
from ui.button import Button
from ui.font_ui import Font_ui
class MenuState(BaseState):
    def __init__(self, game_ctx):
        super().__init__(game_ctx)
        self.play_button = Button(game_ctx.adapter.w_percent(30),game_ctx.adapter.h_percent(45),
        game_ctx.adapter.w_percent(40),game_ctx.adapter.h_percent(8),text="开始游戏")
        self.play_button.set_callbacks(
        on_click=lambda: game_ctx.reset_game(target_state="play", auto_mode=False)
        ) 
        self.introduce_button = Button(game_ctx.adapter.w_percent(30),game_ctx.adapter.h_percent(56),
        game_ctx.adapter.w_percent(40),game_ctx.adapter.h_percent(8),text="游戏介绍")    
        self.introduce_button.set_callbacks(on_click=self.game_ctx.introduce_game)
        self.setting_button = Button(game_ctx.adapter.w_percent(30),game_ctx.adapter.h_percent(67),
        game_ctx.adapter.w_percent(40),game_ctx.adapter.h_percent(8),text="游戏设置(可以调移动模式)")
        self.exit_button = Button(game_ctx.adapter.w_percent(30),game_ctx.adapter.h_percent(78),
        game_ctx.adapter.w_percent(40),game_ctx.adapter.h_percent(8),text="退出游戏")
        self.exit_button.set_callbacks(on_click=self.game_ctx.exit)
        self.setting_button.set_callbacks(on_click=self.game_ctx.change_setting)
    def enter(self):
        for anim in self.game_ctx.animations[:]:
            anim.pause()
    def handle_events(self, event):
        self.play_button.handle_events(event)
        self.exit_button.handle_events(event)
        self.introduce_button.handle_events(event)
        self.setting_button.handle_events(event)     
                
                 
    def render(self):
        if self.game_ctx.move_mode == "joystick":
            self.setting_button.set_text("移动模式：摇杆")
        else:
            self.setting_button.set_text("移动模式：触控")
        self.play_button.draw(self.game_ctx.screen)
        self.exit_button.draw(self.game_ctx.screen)
        self.introduce_button.draw(self.game_ctx.screen)
        self.setting_button.draw(self.game_ctx.screen)
        text="Airplane"    
        font=Font_ui(self.game_ctx,text,200)
        font.prep_font(start=self.game_ctx.adapter.h_percent(20))
        text="Battle!"    
        font=Font_ui(self.game_ctx,text,200)
        font.prep_font(start=self.game_ctx.adapter.h_percent(25))
        text="游戏版本1.0"    
        font=Font_ui(self.game_ctx,text,72)
        font.prep_font(start=self.game_ctx.adapter.h_percent(35))