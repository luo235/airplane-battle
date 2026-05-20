import pygame
from settings import Settings
from game import GameContext

def run_game():
    pygame.mixer.pre_init(
         frequency=44100,
         size=-16,
         channels=2,
         buffer=256
     )
    pygame.init()  
    info = pygame.display.Info()
    physical_w = info.current_w  
    physical_h = info.current_h  
    screen=pygame.display.set_mode((physical_w, physical_h),pygame.NOFRAME)       
    pygame.display.set_caption("Airplane")
    clock=pygame.time.Clock()
    settings=Settings()
    game_ctx = GameContext(screen, settings, clock)
    # 开启AI操控是否
    game_ctx.auto_test_mode = False
    game_ctx.change_state("menu")
    
    #游戏主循环
    while True:
         current_time = pygame.time.get_ticks()
         clock.tick(60)
         game_ctx.handle_events()
         game_ctx.update(current_time)
         for anim in game_ctx.animations[:]:
             if not anim.finished:
                 anim.update(current_time)
         game_ctx.render() 
         for anim in game_ctx.animations:
             if not anim.finished and not anim.paused:
                 anim.draw(screen)
         pygame.display.flip()
         
         
if __name__ == "__main__":
    run_game()