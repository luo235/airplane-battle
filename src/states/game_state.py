import pygame
from .base_state import BaseState
from sprites.airplane_bullet import Bullet
from sprites.enemy import Enemy
from sprites.enemy_bullets import EnemyBullet
from ui.button import Button
from animation import Animation
import random
from sprites.boss import Boss
import math
#遗传算法用的ai
def auto_player_control(game_ctx):
    airplane = game_ctx.airplane
    move_speed = airplane.speed
    if game_ctx.ai_dodge_cooldown > 0:
        game_ctx.ai_dodge_cooldown -= 16.7
        airplane.rect.x += game_ctx.dodge_dir * move_speed
    else:
        danger = False
        for enemy in game_ctx.enemys:
            if abs(enemy.rect.centerx - airplane.rect.centerx) < 50:
                dy = airplane.rect.centery - enemy.rect.centery
                if -20 < dy < 50:  
                    danger = True
                    break  

        if not danger:
            for b in game_ctx.enemy_bullets:
                if b.rect.y > airplane.rect.y:
                    continue
                if abs(b.rect.centerx - airplane.rect.centerx) < 40:
                    dy = airplane.rect.y - b.rect.y
                    if dy < 80:
                        danger = True
                        break
        if danger:
            game_ctx.dodge_dir = random.choice([-1, 1])
            game_ctx.ai_dodge_cooldown = 400
        else:
            game_ctx.dodge_dir = 0
    if game_ctx.dodge_dir == 0:
        target_enemy = None
        min_dist = float('inf')
        for enemy in game_ctx.enemys:
            dx = airplane.rect.centerx - enemy.rect.centerx
            dy = airplane.rect.centery - enemy.rect.centery
            dist = dx * dx + dy * dy
            if dist < min_dist:
                min_dist = dist
                target_enemy = enemy
        if target_enemy is not None:
            if airplane.rect.centerx < target_enemy.rect.centerx - 10:
                airplane.rect.x += move_speed
            elif airplane.rect.centerx > target_enemy.rect.centerx + 10:
                airplane.rect.x -= move_speed
    if airplane.rect.left < 0:
        airplane.rect.left = 0
    if airplane.rect.right > game_ctx.screen_rect.right:
        airplane.rect.right = game_ctx.screen_rect.right


class GameState(BaseState):
    #状态机基本流程
    def enter(self):
        self.game_ctx.play_bgm()
        self.game_ctx.button.set_callbacks(on_click=self.game_ctx.pause)

    def exit(self):
        self.game_ctx.stop_bgm()
    
    def handle_events(self, event):
        #这个按钮是暂停按钮
        self.game_ctx.button.handle_events(event,100,100)
        if self.game_ctx.move_mode == "joystick":
            self.game_ctx.joystick.handle_events(event)
        if self.game_ctx.move_mode == "touch":
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.MOUSEMOTION:
                if event.buttons[0]:
                    self._check_keydown_events(event)     
            elif event.type == pygame.MOUSEBUTTONUP:
                self._check_keyup_events(event)
    
    def update(self, current_time):
        #遗传算法不重要
        if self.game_ctx.auto_test_mode:
            self.game_ctx.sim_time += 16
            current_time = self.game_ctx.sim_time
        if self.game_ctx.auto_test_mode:
            auto_player_control(self.game_ctx)
        #正式流程    
        if not self.game_ctx.auto_test_mode:
            if self.game_ctx.move_mode == "joystick":
                self.game_ctx.airplane.joystick_update_airplane(
                self.game_ctx.joystick.dx,
                self.game_ctx.joystick.dy,
                self.game_ctx.joystick.knob_r
                )
            elif self.game_ctx.move_mode == "touch":
                self.game_ctx.airplane._update_airplane()
        self.creat_one_bullet(current_time)
        self.creat_one_left_bullet(current_time)
        self.creat_one_right_bullet(current_time)
        self.creat_one_left_top_bullet(current_time)
        self.creat_one_right_top_bullet(current_time)
        self.check_boss_occur()
        if not self.game_ctx.boss_occur:
            self.creat_one_enemy(current_time)
            self.creat_one_enemy_bullet(current_time)
        else:
            self.creat_boss_bullet(current_time)
            self.creat_boss_fan_bullets(current_time)
            self.creat_boss_laser(current_time)
        self.update_boss_laser(current_time)    
        self.creat_one_enemy_bullet(current_time)
        self._check_airplane_enemy_collision(current_time)
        if self.game_ctx.current_state is not self:
            return
        self._check_airplane_boss_collision(current_time)    
        if self.game_ctx.current_state is not self:
            return
        self.check_airplane_level()
        if self.game_ctx.current_state is not self:
            return
        self._update_enemy()
        self.game_ctx.boss.update()
        self._update_airplane_bullets(current_time)
        if self.game_ctx.current_state is not self:
            return
        self._update_enemy_bullets()
        if self.game_ctx.current_state is not self:
            return
        self.game_ctx.hud.prep_score()

    def render(self):
        self.game_ctx.button.draw(self.game_ctx.button_surface)
        self.game_ctx.button.draw_line()
        for b in self.game_ctx.bullets.sprites():
            b.draw_bullet()
        for boss in self.game_ctx.boss.sprites():
            boss.blit_boss()
            boss.draw_hp()  
        self.draw_boss_laser()    
        for e in self.game_ctx.enemys.sprites():
            e.blit_enemy()
            e.draw_hp()
        for b in self.game_ctx.enemy_bullets.sprites():
            b.draw_bullet()
        self.game_ctx.airplane.blit_airplane()
        self.game_ctx.airplane.draw_hp()
        self.game_ctx.airplane.draw_xp() 
        self.game_ctx.hud.show_score()  
        if self.game_ctx.move_mode == "joystick":
            self.game_ctx.joystick.draw()
        self.game_ctx.screen.blit(self.game_ctx.button_surface,(100,100))    
    #触屏移动函数
    def _check_keydown_events(self, event):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        airplane = self.game_ctx.airplane
        airplane.moving_bottom = False
        airplane.moving_top = False
        airplane.moving_left = False
        airplane.moving_right = False
        if mouse_x < airplane.rect.x: airplane.moving_left = True
        if mouse_x > airplane.rect.x: airplane.moving_right = True
        if mouse_y > airplane.rect.y: airplane.moving_bottom = True
        if mouse_y < airplane.rect.y: airplane.moving_top = True
        
    def _check_keyup_events(self, event):
        airplane = self.game_ctx.airplane
        airplane.moving_bottom = airplane.moving_top = False
        airplane.moving_left = airplane.moving_right = False
    #爆炸动画
    def add_explosion(self, x, y):
        animation = Animation(self.game_ctx.frames,x,y,fade_out=True,anchor="center")
        def on_finish(anim=animation):
            if anim in self.game_ctx.animations:
                self.game_ctx.animations.remove(anim)
        animation.on_finish = on_finish
        self.game_ctx.animations.append(animation)          
    #碰撞检测
    def _check_airplane_enemy_collision(self,current_time):
        hits = pygame.sprite.spritecollide(self.game_ctx.airplane, self.game_ctx.enemys, True)
        if hits:
            self.game_ctx.play_boom()
            for e in hits:
                self.add_explosion(e.rect.centerx, e.rect.centery)
                damage = ((self.game_ctx.settings.collision_atk+ self.game_ctx.settings.collision_atk_per_level * self.game_ctx.enemy_level)
                         * self.game_ctx.collision_percent- self.game_ctx.defence * 4)
                self.game_ctx.airplane.hp -= damage
                self.game_ctx.airplane.hp = min(self.game_ctx.airplane.hp, self.game_ctx.airplane.max_hp)
                self.game_ctx.hud.score += 100
                if self.game_ctx.kill_add_max_hp:
                    self.game_ctx.airplane.max_hp += self.game_ctx.enemy_level/3
                self.game_ctx.airplane.xp += 10 + self.game_ctx.xp_add * 2.9
                self.game_ctx.count_tool.increase("enemy_death")
                if self.game_ctx.coll_advance==True:
                    self.game_ctx.collision_percent-=0.005
                    self.game_ctx.collision_percent=max(0.09,self.game_ctx.collision_percent)
                if self.game_ctx.airplane.hp <= 0:
                    self.game_ctx.game_over = True
                    self.game_ctx.change_state("game_over")     
    def _check_airplane_boss_collision(self, current_time):
        if not self.game_ctx.boss_occur:
            return
        if self.game_ctx.boss_defeated:
            return
        if self.game_ctx.boss.sprite is None:
            return
        boss = self.game_ctx.boss.sprite
        airplane = self.game_ctx.airplane
        if airplane.rect.colliderect(boss.rect):
            if self.game_ctx.boss_collision_cd.ready(current_time):
                damage = self.game_ctx.settings.boss_collision_atk*self.game_ctx.collision_percent- self.game_ctx.defence * 4
                airplane.hp -= damage
                airplane.hp = min(airplane.hp, airplane.max_hp)
                boss.hp -= 50
                self.game_ctx.boss_collision_cd.reset(current_time)
                if boss.hp <= 0:
                    self.game_ctx.play_boom()
                    self.add_explosion(boss.rect.centerx, boss.rect.centery)
                    self.game_ctx.boss.empty()
                    self.game_ctx.boss_occur = False
                    self.game_ctx.boss_defeated = True
                    self.game_ctx.hud.score += 4000
                    self.game_ctx.change_state("win")
                    return
                if airplane.hp <= 0:
                    self.game_ctx.game_over = True
                    self.game_ctx.change_state("game_over")
                    return                 
    #敌机生成及子弹     
    def creat_one_enemy(self, current_time):
        if self.game_ctx.enemy_cd.ready(current_time):
            new_enemy = Enemy(self.game_ctx)
            collision = any(new_enemy.rect.colliderect(e.rect) for e in self.game_ctx.enemys)
            if not collision:
                base_level = self.game_ctx.enemy_count // 24
                self.game_ctx.enemy_level = max(0,base_level + self.game_ctx.enemy_level_offset)
                new_enemy.hp = self.game_ctx.settings.enemy_hp_per_level * self.game_ctx.enemy_level + self.game_ctx.settings.enemy_hp
                new_enemy.max_hp = self.game_ctx.settings.enemy_max_hp_per_level * self.game_ctx.enemy_level + self.game_ctx.settings.enemy_max_hp
                new_enemy.speed = self.game_ctx.settings.enemy_speed + self.game_ctx.settings.enemy_speed_per_level * self.game_ctx.enemy_level
                if self.game_ctx.settings.enemy_calm_time >= 1000:
                    self.game_ctx.settings.enemy_calm_time -= self.game_ctx.settings.enemy_calm_time_reduce
                if self.game_ctx.settings.enemy_bullet_calm_time >= 1000:
                    self.game_ctx.settings.enemy_bullet_calm_time -= self.game_ctx.settings.enemy_bullet_calm_time_reduce
                self.game_ctx.enemys.add(new_enemy)
                self.game_ctx.enemy_count += 1
                self.game_ctx.enemy_cd.reset(current_time)
                
    def _update_enemy(self):
        self.game_ctx.enemys.update()
        for e in self.game_ctx.enemys.copy():
            if e.rect.top >= self.game_ctx.screen_rect.height:
                self.game_ctx.enemys.remove(e)         
                
    def creat_one_enemy_bullet(self,current_time):
        if self.game_ctx.enemy_bullet_cd.ready(current_time):
            for e in self.game_ctx.enemys:
                eb = EnemyBullet(self.game_ctx, e)
                eb.atk = self.game_ctx.settings.enemy_bullet_atk + 5*self.game_ctx.enemy_level
                eb.speed = self.game_ctx.settings.enemy_bullet_speed + 0.5*self.game_ctx.enemy_level - 0.6*self.game_ctx.lower_enemy_bullet_speed
                self.game_ctx.enemy_bullets.add(eb)
            self.game_ctx.enemy_bullet_cd.reset(current_time)          
            
    def _update_enemy_bullets(self):
        self.game_ctx.enemy_bullets.update()
        for b in self.game_ctx.enemy_bullets.copy():
            if (
               b.rect.top > self.game_ctx.screen_rect.bottom
               or b.rect.right < 0
               or b.rect.left > self.game_ctx.screen_rect.right
               ):
                self.game_ctx.enemy_bullets.remove(b)
        hits = pygame.sprite.spritecollide(self.game_ctx.airplane, self.game_ctx.enemy_bullets, True)
        if hits:
            for b in hits:
                self.game_ctx.airplane.hp -= b.atk - self.game_ctx.defence * 4
                self.game_ctx.airplane.hp = min(self.game_ctx.airplane.hp, self.game_ctx.airplane.max_hp)
                if self.game_ctx.airplane.hp <= 0:
                    self.game_ctx.game_over = True
                    self.game_ctx.change_state("game_over")
    #检测飞机升级
    def check_airplane_level(self):
        if self.game_ctx.airplane.xp >= self.game_ctx.airplane.max_xp:
            self.game_ctx.airplane.xp -= self.game_ctx.airplane.max_xp
            self.game_ctx.airplane.max_xp += self.game_ctx.settings.airplane_max_xp_add
            self.game_ctx.airplane_level += 1
            self.game_ctx.airplane.max_hp += self.game_ctx.settings.airplane_max_hp_add
            self.game_ctx.airplane.hp += self.game_ctx.settings.airplane_hp_add
            self.game_ctx.settings.airplane_bullet_atk += self.game_ctx.settings.airplane_bullet_atk_add
            if self.game_ctx.airplane_level % 3 == 0:
                self.game_ctx.high_event = True
            self.game_ctx.change_state("level_choose") 
    #创建各飞机子弹             
    def creat_one_bullet(self,current_time):
        if self.game_ctx.bullet_cd.ready(current_time):
            self.game_ctx.play_shot()
            self.game_ctx.bullets.add(Bullet(self.game_ctx))
            self.game_ctx.bullet_cd.reset(current_time)
            
    def creat_one_left_bullet(self,current_time):
        if self.game_ctx.left_add_bullet:
            if self.game_ctx.left_bullet_cd.ready(current_time):
                b = Bullet(self.game_ctx)
                b.rect.x -= 30
                b.x = float(b.rect.x)
                self.game_ctx.bullets.add(b)
                self.game_ctx.left_bullet_cd.reset(current_time)
                
    def creat_one_right_bullet(self,current_time):
        if self.game_ctx.right_add_bullet:
            if self.game_ctx.right_bullet_cd.ready(current_time):
                b = Bullet(self.game_ctx)
                b.rect.x += 30
                b.x = float(b.rect.x)
                self.game_ctx.bullets.add(b)
                self.game_ctx.right_bullet_cd.reset(current_time)
                
    def creat_one_left_top_bullet(self,current_time):
        if self.game_ctx.left_top_add_bullet:
            if self.game_ctx.left_top_bullet_cd.ready(current_time):
                b = Bullet(self.game_ctx)
                b.rect.x -= 60
                b.x = float(b.rect.x)
                b.direction = -1
                self.game_ctx.bullets.add(b)
                self.game_ctx.left_top_bullet_cd.reset(current_time)
                
    def creat_one_right_top_bullet(self,current_time):
        if self.game_ctx.right_top_add_bullet: 
            if self.game_ctx.right_top_bullet_cd.ready(current_time):
                b = Bullet(self.game_ctx)
                b.rect.x += 60
                b.x = float(b.rect.x)
                b.direction = 1
                self.game_ctx.bullets.add(b)
                self.game_ctx.right_top_bullet_cd.reset(current_time)
                
    def _update_airplane_bullets(self, current_time):
        self.game_ctx.bullets.update()
        for b in self.game_ctx.bullets.copy():
            if b.rect.bottom < 0:
                self.game_ctx.bullets.remove(b)
        for b in self.game_ctx.bullets.copy():
            hits = pygame.sprite.spritecollide(b, self.game_ctx.enemys, False)
            if hits:
                if b in self.game_ctx.bullets:
                    self.game_ctx.bullets.remove(b)
                for e in hits:
                    e.hp -= b.atk
                    self.game_ctx.airplane.hp += b.atk * self.game_ctx.lifesteal
                    self.game_ctx.airplane.hp = min(
                        self.game_ctx.airplane.hp,
                        self.game_ctx.airplane.max_hp
                    )
                    if e.hp <= 0:
                        self.game_ctx.play_boom()
                        self.add_explosion(e.rect.centerx, e.rect.centery)
                        self.game_ctx.count_tool.increase("enemy_death")
                        self.game_ctx.enemys.remove(e)
                        self.game_ctx.hud.score += 100
                        self.game_ctx.airplane.xp += 10 + self.game_ctx.xp_add * 2.9
                        if self.game_ctx.kill_add_max_hp:
                            self.game_ctx.airplane.max_hp += self.game_ctx.enemy_level/3
                continue
            if self.game_ctx.boss.sprite:
                boss = self.game_ctx.boss.sprite
                if b.rect.colliderect(boss.rect):
                    if b in self.game_ctx.bullets:
                        self.game_ctx.bullets.remove(b)
                    boss.hp -= b.atk
                    self.game_ctx.airplane.hp += b.atk * self.game_ctx.lifesteal
                    self.game_ctx.airplane.hp = min(
                        self.game_ctx.airplane.hp,
                        self.game_ctx.airplane.max_hp
                    )
                    if boss.hp <= 0:
                        self.game_ctx.play_boom()
                        self.add_explosion(boss.rect.centerx, boss.rect.centery)
                        self.game_ctx.boss.empty()
                        self.game_ctx.boss_occur = False
                        self.game_ctx.boss_defeated = True
                        self.game_ctx.hud.score += 3000
                        self.game_ctx.change_state("win")
                        return             
    #boss及子弹
    def check_boss_occur(self):
        if self.game_ctx.boss_occur:
            return
        if self.game_ctx.boss_defeated:
            return
        if self.game_ctx.survive_time >= self.game_ctx.boss_time:
            boss = Boss(self.game_ctx)
            self.game_ctx.boss.add(boss)
            self.game_ctx.boss_occur = True
            self.game_ctx.enemys.empty()
            self.game_ctx.settings.enemy_bullet_atk = self.game_ctx.settings.boss_enemy_bullet_atk
            self.game_ctx.settings.enemy_bullet_speed = self.game_ctx.settings.boss_enemy_bullet_speed
    
    def creat_boss_bullet(self, current_time):
        if not self.game_ctx.boss_occur:
            return
        if self.game_ctx.boss_defeated:
            return
        if self.game_ctx.boss.sprite is None:
            return
        if self.game_ctx.boss_bullet_cd.ready(current_time):
            boss = self.game_ctx.boss.sprite
            eb = EnemyBullet(self.game_ctx, boss)
            self.game_ctx.enemy_bullets.add(eb)
            self.game_ctx.boss_bullet_cd.reset(current_time)
            
    def creat_boss_fan_bullets(self, current_time):
        if not self.game_ctx.boss_occur:
            return
        if self.game_ctx.boss_defeated:
            return
        if self.game_ctx.boss.sprite is None:
            return
        if not self.game_ctx.boss_fan_bullet_cd.ready(current_time):
            return
        boss = self.game_ctx.boss.sprite
        count = self.game_ctx.settings.boss_fan_bullet_count
        speed = self.game_ctx.settings.boss_fan_bullet_speed
        total_angle = self.game_ctx.settings.boss_fan_bullet_angle
        start_angle = -total_angle / 2
        step = total_angle / (count - 1)
        angles = [start_angle + step * i for i in range(count)]
        for angle in angles:
            rad = math.radians(angle)
            eb = EnemyBullet(self.game_ctx, boss)
            eb.speed_x = math.sin(rad) * speed
            eb.speed = math.cos(rad) * speed
            eb.x = float(eb.rect.x)
            eb.y = float(eb.rect.y)
            self.game_ctx.enemy_bullets.add(eb)
        self.game_ctx.boss_fan_bullet_cd.reset(current_time)    
            
    def creat_boss_laser(self, current_time):
        if not self.game_ctx.boss_occur:
            return
        if self.game_ctx.boss_defeated:
            return
        if self.game_ctx.boss.sprite is None:
            return
        if self.game_ctx.boss_laser_warning:
            return
        if self.game_ctx.boss_laser_active:
            return
        if self.game_ctx.boss_laser_cd.ready(current_time):
            self.game_ctx.boss_laser_x = self.game_ctx.airplane.rect.centerx
            self.game_ctx.boss_laser_warning = True
            self.game_ctx.boss_laser_active = False
            self.game_ctx.boss_laser_start_time = current_time
            self.game_ctx.boss_laser_hit = False
    def update_boss_laser(self, current_time):
        if self.game_ctx.boss_laser_warning:
            if current_time - self.game_ctx.boss_laser_start_time >= self.game_ctx.settings.boss_laser_warning_time:
                self.game_ctx.boss_laser_warning = False
                self.game_ctx.boss_laser_active = True
                self.game_ctx.boss_laser_start_time = current_time
                self.game_ctx.boss_laser_hit = False
        if self.game_ctx.boss_laser_active:
            laser_width = self.game_ctx.settings.boss_laser_width
            laser_x = self.game_ctx.boss_laser_x
            laser_rect = pygame.Rect(
                laser_x - laser_width // 2,
                0,
                laser_width,
                self.game_ctx.screen_rect.height
            )
            if not self.game_ctx.boss_laser_hit:
                if laser_rect.colliderect(self.game_ctx.airplane.rect):
                    damage = self.game_ctx.settings.boss_laser_atk - self.game_ctx.defence * 4
                    self.game_ctx.airplane.hp -= damage
                    self.game_ctx.airplane.hp = min(
                        self.game_ctx.airplane.hp,
                        self.game_ctx.airplane.max_hp
                    )
                    self.game_ctx.boss_laser_hit = True
                    if self.game_ctx.airplane.hp <= 0:
                        self.game_ctx.game_over = True
                        self.game_ctx.change_state("game_over")
                        return
            if current_time - self.game_ctx.boss_laser_start_time >= self.game_ctx.settings.boss_laser_active_time:
                self.game_ctx.boss_laser_active = False
                self.game_ctx.boss_laser_cd.reset(current_time)   
                 
    def draw_boss_laser(self):
        laser_width = self.game_ctx.settings.boss_laser_width
        laser_x = self.game_ctx.boss_laser_x
        x = laser_x - laser_width // 2
        y = 0
        h = self.game_ctx.screen_rect.height
        laser_surface = pygame.Surface(
            (laser_width, h),
            pygame.SRCALPHA
        )
        if self.game_ctx.boss_laser_warning:
            pygame.draw.rect(
                laser_surface,
                (255, 0, 0, 80),
                (0, 0, laser_width, h)
            )
            pygame.draw.rect(
                laser_surface,
                (255, 0, 0, 180),
                (laser_width // 2 - 2, 0, 4, h)
            )
            self.game_ctx.screen.blit(laser_surface, (x, y))
        if self.game_ctx.boss_laser_active:
            pygame.draw.rect(
                laser_surface,
                (255, 0, 0, 180),
                (0, 0, laser_width, h)
            )
            pygame.draw.rect(
                laser_surface,
                (255, 255, 255, 220),
                (laser_width // 2 - 4, 0, 8, h)
            )
            self.game_ctx.screen.blit(laser_surface, (x, y))        