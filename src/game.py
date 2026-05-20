import pygame
import sys
from sprites.airplane import Airplane
from ui.hud import HUD
from states.menu_state import MenuState
from states.game_state import GameState
from states.level_choose_state import LevelChooseState
from utils.timer_tool import CoolDown
from states.game_over_state import GameOverState
from utils.count_tool import Count_tool
from utils.adapter import ScreenAdapter
from ui.joystick import JoyStick
from ui.button import Button
from states.gamepause_state import GamePause
from utils.sheet_tool import Sheet
from states.win_state import WinState
from states.introduce_state import IntroState
class GameContext:
    def __init__(self, screen, settings, clock):
        #遗传算法
        self.auto_test_mode = False
        self.sim_time = 0  
        self.ai_dodge_cooldown = 0
        self.dodge_dir = 0
        #一些基础设置
        self.screen = screen
        self.screen_rect = self.screen.get_rect()  
        self.settings=settings
        self.default_settings = self.settings.__dict__.copy()
        self.animations=[]
        self.game_over = False  
        self.survive_time = 0  
        #移动方式
        self.move_mode = "joystick"
        #音效
        self.bgm_path = "resource/sound/cool.ogg"
        self.shot_sound = pygame.mixer.Sound("resource/sound/shot.ogg")
        self.boom_sound = pygame.mixer.Sound("resource/sound/boom.wav")
        self.shot_sound.set_volume(0.4)
        self.boom_sound.set_volume(0.2)
        #工具
        self.count_tool=Count_tool()
        self.adapter = ScreenAdapter(self.screen_rect.width, self.screen_rect.height)
        self.frames=Sheet.load_sprite_sheet("resource/images/explosion 4.png",512,512,scale=(250,250))
        self.frames=self.frames[2:]
        #摇杆
        self.joystick=JoyStick(self.screen,base_pos=(self.adapter.w_percent(30),self.adapter.h_percent(87)))
        #按钮
        self.button_surface=pygame.Surface((100,100),pygame.SRCALPHA)
        self.button = Button(
             0, 0, 100, 100,
             border_radius=50,
             color=(40, 40, 40,150),        
            hover_color=(80, 80, 80,150),  
             click_color=(20,20, 20,150),
             icon_type='pause',
             font_size=72,
         )
        #分数ui
        self.hud = HUD(self)
        
        # 飞机及子弹
        self.airplane = Airplane(self)
        self.airplane_level = 2
        self.bullets = pygame.sprite.Group()
        #有关飞机的技能属性
        self.defence = 0
        self.collision_percent = 1.0
        self.lifesteal = 0.0
        self.xp_add = 0
        self.coll_advance=False
        self.high_event = False
        self.left_add_bullet = False          
        self.right_add_bullet = False
        self.left_top_add_bullet = False
        self.right_top_add_bullet = False
        self.left_bullet_unlocked = False
        self.right_bullet_unlocked = False
        self.left_top_bullet_unlocked = False
        self.right_top_bullet_unlocked = False
        self.kill_add_max_hp = False
        #飞机子弹cd
        self.bullet_cd = CoolDown(lambda: self.settings.bullet_calm_time)
        self.left_bullet_cd = CoolDown(lambda: self.settings.bullet_calm_time)
        self.right_bullet_cd = CoolDown(lambda: self.settings.bullet_calm_time)
        self.left_top_bullet_cd = CoolDown(lambda: self.settings.bullet_calm_time)
        self.right_top_bullet_cd = CoolDown(lambda: self.settings.bullet_calm_time)
            
        # 敌人及子弹
        self.enemys = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.enemy_level = 0
        self.enemy_count = 0  
        #有关针对敌人的技能的属性
        self.lower_enemy_bullet_speed = 0  
        self.enemy_level_offset = 0
        #敌机cd
        self.enemy_cd = CoolDown(lambda: self.settings.enemy_calm_time)
        self.enemy_bullet_cd = CoolDown(lambda: self.settings.enemy_bullet_calm_time)
        #boss
        self.boss = pygame.sprite.GroupSingle()
        self.boss_occur = False
        self.boss_defeated = False
        self.boss_time=420000
        self.boss_laser_cd = CoolDown(lambda: self.settings.boss_laser_calm_time)
        self.boss_laser_warning = False
        self.boss_laser_active = False
        self.boss_laser_start_time = 0
        self.boss_laser_x = 0
        self.boss_laser_hit = False
        #boss cd
        self.boss_bullet_cd = CoolDown(lambda: self.settings.boss_bullet_calm_time)
        self.boss_fan_bullet_cd = CoolDown(lambda: self.settings.boss_fan_bullet_calm_time)   
        self.boss_collision_cd = CoolDown(500)
        
        #状态机
        self.current_state = None  
        self.states = {
             "menu": MenuState(self),
             "play": GameState(self),
             "level_choose": LevelChooseState(self) ,
              "game_over":  GameOverState(self)  ,
              "pause"  :     GamePause(self),
              "win": WinState(self),    
              "intro": IntroState(self),
         }
         
    #一些状态机函数    
    def change_state(self, state_name):
        if self.current_state:
            self.current_state.exit()
        self.current_state = self.states[state_name]
        self.current_state.enter()
    def pause(self) :
        self.change_state("pause")   
    def resume(self) :
        self.change_state("play")   
    #每个状态机的基本流程    
    def handle_events(self):
         for event in pygame.event.get():
             if event.type == pygame.QUIT:
                 pygame.quit()
                 sys.exit()
             if self.current_state:
                 self.current_state.handle_events(event)
    def update(self, current_time):
        if self.current_state:
            if self.current_state == self.states["play"]:
                self.survive_time += 16.67  
            self.current_state.update(current_time)
    def render(self):
        self.screen.fill((230, 230, 230))
        if self.current_state:
            self.current_state.render()     
    #一些基础功能          
    def play_bgm(self):
         pygame.mixer.music.load(self.bgm_path)
         pygame.mixer.music.set_volume(0.3)  
         pygame.mixer.music.play(-1) 
    def stop_bgm(self):
         pygame.mixer.music.stop()
    def play_shot(self):
        self.shot_sound.play()
    def play_boom(self):
        self.boom_sound.play()      
    def exit(self) :
        sys.exit(0)
    def introduce_game(self) :
        self.change_state("intro")
    def change_setting(self):
        if self.move_mode == "joystick":
            self.move_mode = "touch"
        else:
            self.move_mode = "joystick"
    
    #重置游戏设置
    def reset_game(self, now=None, target_state="play", auto_mode=False, reset_settings=True):
        if now is None:
            now = pygame.time.get_ticks()
        #恢复 settings
        if reset_settings:
            for key, value in self.default_settings.items():
                setattr(self.settings, key, value)
        #重置飞机
        self.airplane.max_hp = self.settings.airplane_max_hp
        self.airplane.hp = self.airplane.max_hp
        self.airplane.speed = self.settings.airplane_speed
        self.airplane.hp_heal = 0.01
        self.airplane.xp = 0
        self.airplane.max_xp = 100
        self.airplane.rect.centerx = self.screen.get_width() // 2
        self.airplane.rect.bottom = self.screen.get_height() - 50
        self.airplane.x = float(self.airplane.rect.x)
        self.airplane.y = float(self.airplane.rect.y)
        #清空场上对象
        self.bullets.empty()
        self.enemys.empty()
        self.enemy_bullets.empty()
        self.animations.clear()
        self.boss.empty()
        #重置游戏状态
        self.hud.score = 0
        self.enemy_count = 0
        self.enemy_level = 0
        self.airplane_level = 2
        self.survive_time = 0
        self.sim_time = 0
        self.game_over = False
        self.high_event = False
        self.boss_occur = False
        self.boss_defeated = False
        self.boss_laser_warning = False
        self.boss_laser_active = False
        self.boss_laser_start_time = 0
        self.boss_laser_x = 0
        self.boss_laser_hit = False
        self.coll_advance=False
        #重置技能状态
        self.defence = 0
        self.collision_percent = 1.0
        self.lifesteal = 0.0
        self.xp_add = 0
        self.lower_enemy_bullet_speed = 0
        self.enemy_level_offset = 0
        self.left_add_bullet = False
        self.right_add_bullet = False
        self.left_top_add_bullet = False
        self.right_top_add_bullet = False
        self.kill_add_max_hp = False
        self.left_bullet_unlocked = False
        self.right_bullet_unlocked = False
        self.left_top_bullet_unlocked = False
        self.right_top_bullet_unlocked = False
        #重置统计
        self.count_tool.all_name["enemy_count"] = 0
        self.count_tool.all_name["enemy_death"] = 0
        self.count_tool.all_name["shoot_count"] = 0
        #重置冷却起点
        self.bullet_cd.reset(now)
        self.enemy_cd.reset(now)
        self.enemy_bullet_cd.reset(now)
        self.left_bullet_cd.reset(now)
        self.right_bullet_cd.reset(now)
        self.left_top_bullet_cd.reset(now)
        self.right_top_bullet_cd.reset(now)
        self.boss_bullet_cd.reset(now)
        self.boss_fan_bullet_cd.reset(now)
        self.boss_laser_cd.reset(now)
        self.boss_collision_cd.reset(now)
        #AI模式
        self.auto_test_mode = auto_mode
        self.ai_dodge_cooldown = 0
        self.dodge_dir = 0
        self.last_bullet_time = 0
        #切换状态
        if target_state:
            self.change_state(target_state)