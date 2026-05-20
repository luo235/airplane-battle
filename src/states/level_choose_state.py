import pygame
import random
from .base_state import BaseState
from ui.button import Button

class LevelChooseState(BaseState):
    #状态机基本流程
    def enter(self):
        self.random_3_event()
        for anim in self.game_ctx.animations[:]:
            anim.pause()
        if self.game_ctx.auto_test_mode:
             self.event_funcs[0]()
             self.game_ctx.change_state("play")     
    def exit(self):
        for anim in self.game_ctx.animations[:]:
            anim.resume()    
    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for i, btn in enumerate(self.event_buttons):
                if btn.rect.collidepoint(mouse_pos):
                    self.event_funcs[i]()
                    self.game_ctx.change_state("play")
            
    def render(self):
        for btn in self.event_buttons:
            btn.draw(self.game_ctx.screen)       
    #随机技能         
    def random_3_event(self):
        if not self.game_ctx.high_event:
            events = [
                ("穿上草鞋飞一般的感觉(加快飞机移速)", self.accelerate_airplane_speed),
                ("此生此武天下无双(加子弹伤害)", self.increase_bullet_atk),
                ("我的血条好像超出屏幕了(加血量)", self.increase_hp),
                ("是时候掏出我的加特林了(加主子弹攻速)", self.increase_attack_speed),
                ("贤者我有才艺(加回血)", self.increase_heal),
                ("太极生两仪(加防御，防高挨打会回血)", self.lower_enemy_atk),
                ("子弹时间(敌人子弹速度下降，发射频率减少)", self.lower_enemy_bullet),
                ("幸运女神在微笑(下次升级变为高级技能选项)", self.level_up_event),
                ("达尔文事变(敌人等级减1)", self.lower_enemy_level),
                ("我独自升级(获取经验加速)", self.increase_xp),
                ("我一颗子弹有屏幕那么大(子弹宽度增加)", self.increase_bullet_width_func)
            ]
        else:
            events = [
                ("鲜血杀戮使我沸腾(加子弹吸血,杀敌加最大生命)", self.increase_Lifesteal),
                ("乱拳打死老师傅(左)(解锁左副弹,降低攻速,降低攻击)", self.left_add_bullet_event),
                ("乱拳打死老师傅(右)(解锁右副弹,降低攻速,降低攻击)", self.right_add_bullet_event),
                ("乱拳打死老师傅(左上)(解锁左上副弹,降低攻速,降低攻击)", self.left_top_add_bullet_event),
                ("乱拳打死老师傅(右上)(解锁右上副弹,降低攻速,降低攻击)", self.right_top_add_bullet_event),
                ("I am atomic(清除全场敌人)",self.atomic),
                ("恶魔契约(将血量降低为一，扣除血量转换为经验)",self.hp_transform_xp),
                ("金钟罩铁布衫(降低碰撞伤害，减少自己子弹伤害)", self.lower_collision),
                ("碰碰车(碰撞击杀敌人增加碰撞伤害减免(注碰撞伤害减免有上限))",self.collision_advance),
            ]
            
            if self.game_ctx.right_top_bullet_unlocked: del events[4]
            if self.game_ctx.left_top_bullet_unlocked: del events[3]
            if self.game_ctx.right_bullet_unlocked: del events[2]
            if self.game_ctx.left_bullet_unlocked: del events[1]
            self.game_ctx.high_event = False
            
        selected = random.sample(events, min(3, len(events)))
        self.event_buttons = []
        self.event_funcs = []
        for i, (msg, func) in enumerate(selected):
            btn = Button(self.game_ctx.adapter.w_percent(15),self.game_ctx.adapter.h_percent(10+i*30),self.game_ctx.adapter.w_percent(70),self.game_ctx.adapter.h_percent(20),text=msg)
            self.event_buttons.append(btn)
            self.event_funcs.append(func)
    #技能池排序按上面技能顺序一一对应     
    def accelerate_airplane_speed(self):
        self.game_ctx.airplane.speed += self.game_ctx.settings.airplane_speed_add
            
    def increase_bullet_atk(self):
        self.game_ctx.settings.airplane_bullet_atk += self.game_ctx.settings.bullet_atk_add
        
    def increase_hp(self):
        s = self.game_ctx.settings
        self.game_ctx.airplane.hp += s.hp_add
        self.game_ctx.airplane.max_hp += s.max_hp_add
        
    def increase_attack_speed(self):
        s = self.game_ctx.settings
        s.bullet_speed += s.bullet_speed_add
        if s.bullet_calm_time >= 100:
            s.bullet_calm_time -= s.bullet_calm_time_sub     
    
    def increase_heal(self):
        self.game_ctx.airplane.hp_heal += self.game_ctx.settings.hp_heal_add

    def lower_enemy_atk(self):
        self.game_ctx.defence += self.game_ctx.settings.defence_add

    def lower_enemy_bullet(self):
        s = self.game_ctx.settings
        s.enemy_bullet_calm_time += s.enemy_bullet_calm_time_add
        self.game_ctx.lower_enemy_bullet_speed += s.lower_enemy_bullet_speed_add
        
    def level_up_event(self):
        self.game_ctx.high_event = True

    def lower_enemy_level(self):
        self.game_ctx.enemy_level_offset -= 1

    def increase_xp(self):
        self.game_ctx.xp_add += self.game_ctx.settings.xp_add_add    
    
    def increase_bullet_width_func(self):
        self.game_ctx.settings.bullet_width += self.game_ctx.settings.bullet_width_add     
            
    def increase_Lifesteal(self):
        self.game_ctx.lifesteal += self.game_ctx.settings.lifesteal_add
        self.game_ctx.kill_add_max_hp = True     
            
    def left_add_bullet_event(self):
        s = self.game_ctx.settings
        self.game_ctx.left_add_bullet = True
        self.game_ctx.left_bullet_unlocked = True
        s.bullet_calm_time += s.bullet_calm_time_add
        s.bullet_speed -= s.bullet_speed_sub
        s.airplane_bullet_atk -= s.airplane_bullet_atk_sub
        
    def right_add_bullet_event(self):
        s = self.game_ctx.settings
        self.game_ctx.right_add_bullet = True
        self.game_ctx.right_bullet_unlocked = True
        s.bullet_calm_time += s.bullet_calm_time_add
        s.bullet_speed -= s.bullet_speed_sub
        s.airplane_bullet_atk -= s.airplane_bullet_atk_sub
        
    def left_top_add_bullet_event(self):
        s = self.game_ctx.settings
        self.game_ctx.left_top_add_bullet = True
        self.game_ctx.left_top_bullet_unlocked = True
        s.bullet_calm_time += s.bullet_calm_time_add
        s.bullet_speed -= s.bullet_speed_sub
        s.airplane_bullet_atk -= s.airplane_bullet_atk_sub
        
    def right_top_add_bullet_event(self):
        s = self.game_ctx.settings
        self.game_ctx.right_top_add_bullet = True
        self.game_ctx.right_top_bullet_unlocked = True
        s.bullet_calm_time += s.bullet_calm_time_add
        s.bullet_speed -= s.bullet_speed_sub
        s.airplane_bullet_atk -= s.airplane_bullet_atk_sub
        
    def atomic(self):
        cnt = len(self.game_ctx.enemys)
        self.game_ctx.enemys.empty()
        self.game_ctx.airplane.xp += cnt*10
        self.game_ctx.hud.score += 100*cnt
        
    def hp_transform_xp(self):
        self.game_ctx.airplane.xp += self.game_ctx.airplane.hp - 1
        self.game_ctx.airplane.hp = 1

    def lower_collision(self):
        s = self.game_ctx.settings
        self.game_ctx.collision_percent -= self.game_ctx.settings.collision_percent
        self.game_ctx.collision_percent = max(0.09, self.game_ctx.collision_percent)
        s.airplane_bullet_atk-=50
        s.airplane_bullet_atk=max(s.airplane_bullet_atk,10)

    def collision_advance(self):
        self.game_ctx.coll_advance=True  