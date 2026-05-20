from .base_state import BaseState
from ui.font_ui import Font_ui
from ui.button import Button

class WinState(BaseState):
    def __init__(self, game_ctx):
        super().__init__(game_ctx)

        self.restart_button = Button(
            game_ctx.adapter.w_percent(30),
            game_ctx.adapter.h_percent(70),
            game_ctx.adapter.w_percent(40),
            game_ctx.adapter.h_percent(8),
            text="再来一局"
        )

        self.menu_button = Button(
            game_ctx.adapter.w_percent(30),
            game_ctx.adapter.h_percent(80),
            game_ctx.adapter.w_percent(40),
            game_ctx.adapter.h_percent(8),
            text="返回主菜单"
        )

        self.restart_button.set_callbacks(
            on_click=lambda: self.game_ctx.reset_game(
                target_state="play",
                auto_mode=False
            )
        )

        self.menu_button.set_callbacks(
            on_click=lambda: self.game_ctx.reset_game(
                target_state="menu",
                auto_mode=False
            )
        )

    def enter(self):
        for anim in self.game_ctx.animations[:]:
            anim.pause()

    def handle_events(self, event):
        self.restart_button.handle_events(event)
        self.menu_button.handle_events(event)

    def render(self):
        text = "You Win!"
        font = Font_ui(self.game_ctx, text, font_size=200)
        font.prep_font(start=120)
        stats_texts = [
            f"你成功击败了Boss",
            f"一共生成了{self.game_ctx.enemy_count}个敌人",
            f"你一共击败了{self.game_ctx.count_tool.all_name['enemy_death']}个敌人",
            f"最终得分：{self.game_ctx.hud.score}",
            f"你的飞机一共升级了{self.game_ctx.airplane_level - 2}次",
            "恭喜通关"
        ]
        font = Font_ui(self.game_ctx, stats_texts, font_size=72)
        font.prep_font(start=300)
        self.restart_button.draw(self.game_ctx.screen)
        self.menu_button.draw(self.game_ctx.screen)