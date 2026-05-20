import pygame
from .base_state import BaseState
from ui.button import Button
from ui.font_ui import Font_ui

class IntroState(BaseState):
    def __init__(self, game_ctx):
        super().__init__(game_ctx)
        self.back_button = Button(
            game_ctx.adapter.w_percent(30),
            game_ctx.adapter.h_percent(82),
            game_ctx.adapter.w_percent(40),
            game_ctx.adapter.h_percent(8),
            text="返回主菜单"
        )
        self.back_button.set_callbacks(
            on_click=lambda: self.game_ctx.change_state("menu")
        )

    def handle_events(self, event):
        self.back_button.handle_events(event)

    def render(self):
        title = Font_ui(self.game_ctx,"Game Introduction", font_size=90)
        title.prep_font(start=120)
        lines = [
        "玩法目标：操控飞机生存、击败敌机、升级强化，最终击败Boss。",
        "移动方式：可在主菜单切换摇杆模式或触控模式。",
        "战斗方式：飞机会自动发射子弹，击败敌人获得分数和经验。",
        "升级系统：升级后可选择移速、攻击、血量、防御、吸血、副弹等能力。",
        "Boss战：生存到指定时间后Boss出现，拥有扇形弹幕和激光预警技能。",
        "胜利条件：击败Boss即可通关。",
        "失败条件：飞机生命值降为0。"
        ]
        text = Font_ui(self.game_ctx,lines,font_size=42)
        text.prep_font(start=250)
        self.back_button.draw(self.game_ctx.screen)