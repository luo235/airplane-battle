class Settings:
    def __init__(self):
        #基础设置
        self.bg_color = (230,230,230)
        self.bullet_color = (60,60,60)
        self.enemy_bullet_color = (255,0,0)
        #飞机子弹设置
        self.bullet_width = 15
        self.bullet_height = 10
        self.bullet_speed = 10
        self.bullet_calm_time = 800
        self.airplane_bullet_atk = 14
        #一些飞机设置
        self.airplane_speed = 5
        self.airplane_max_hp = 100
        #飞机属性成长
        self.airplane_max_xp_add = 4     
        self.airplane_max_hp_add = 12     
        self.airplane_hp_add = 12           
        self.airplane_bullet_atk_add = 5  
        #敌机子弹设置
        self.enemy_bullet_width = 15
        self.enemy_bullet_height = 10
        self.enemy_bullet_speed = 5.5
        self.enemy_bullet_calm_time = 4000
        #敌机属性设置
        self.collision_atk = 80
        self.enemy_bullet_atk = 16
        self.enemy_hp = 14
        self.enemy_max_hp = 14
        self.enemy_speed = 2.7
        self.enemy_calm_time = 2000
        #敌机属性成长
        self.enemy_hp_per_level = 9    
        self.enemy_max_hp_per_level = 9   
        self.enemy_speed_per_level = 0.35  
        self.collision_atk_per_level = 6
        self.enemy_calm_time_reduce = 10    
        self.enemy_bullet_calm_time_reduce = 50  
        #技能选择相关设定
        self.collision_percent = 0.3
        self.bullet_calm_time_add = 300
        self.bullet_speed_sub = 1
        self.airplane_bullet_atk_sub = 1.5
        self.bullet_width_add = 10
        self.lifesteal_add = 0.1
        self.airplane_speed_add = 2
        self.bullet_atk_add = 25
        self.hp_add = 75
        self.max_hp_add = 75
        self.bullet_speed_add = 1.5
        self.bullet_calm_time_sub = 150
        self.hp_heal_add = 0.2
        self.defence_add = 1
        self.enemy_bullet_calm_time_add = 350
        self.lower_enemy_bullet_speed_add = 2
        self.xp_add_add = 2
        #有关boss的基础设置
        self.boss_hp = 1500
        self.boss_max_hp = 1500
        self.boss_speed = 8
        self.boss_bullet_calm_time = 800
        self.boss_collision_atk = 150
        #boss普通子弹设置
        self.boss_enemy_bullet_atk = 110
        self.boss_enemy_bullet_speed = 10
        #boss扇形弹幕设置
        self.boss_fan_bullet_calm_time = 2000
        self.boss_fan_bullet_count = 15
        self.boss_fan_bullet_speed = 8
        self.boss_fan_bullet_angle = 70
        #boss激光设置
        self.boss_laser_calm_time = 4000      
        self.boss_laser_warning_time = 800   
        self.boss_laser_active_time = 900    
        self.boss_laser_width = 150            
        self.boss_laser_atk =500  