import pygame
from utils.timer_tool import CoolDown
class Animation:
    def __init__(self,frames,x,y,fps=60,loop=False,fade_out=False,fade_step=10,on_finish=None,anchor='topleft'):
        self.frames=frames
        self.fps=fps
        self.loop=loop
        self.current_index=0
        self.finished=False
        self.cd=CoolDown(interval=1000/fps)
        self.x=x
        self.y=y
        self.paused=False
        self.paused_time=0
        self.fade_out=fade_out
        self.fade_step=fade_step
        self.alpha=255
        self.on_finish=on_finish
        self.anchor=anchor
    def pause(self):
        if not self.finished and not self.paused:
            self.paused=True
            self.paused_time=pygame.time.get_ticks()
    def resume(self):
        self.paused=False
        delta=pygame.time.get_ticks()-self.paused_time
        self.cd.last+=delta
    
    def update(self,current_time):
        if self.finished or self.paused:
            return
        if self.cd.ready(current_time):
            self.current_index+=3
            if self.current_index>=len(self.frames):
                if self.loop:
                    self.current_index=0
                elif not self.loop :
                    self.current_index=len(self.frames)-1
                    if self.fade_out:
                        self.alpha -= self.fade_step
                        if self.alpha<=0:
                            self.alpha=0
                            self.finished=True
                            if self.on_finish:
                                self.on_finish()
                    else:
                        self.finished=True
                        if self.on_finish:
                            self.on_finish()    
            self.cd.reset(current_time)          
    def draw(self,screen) :
        current_img=self.frames[self.current_index]
        img_copy=current_img.copy()
        draw_x=self.x
        draw_y=self.y
        if self.anchor=="center":
            draw_x-=img_copy.get_width()//2  
            draw_y-=img_copy.get_height()//2
        img_copy.set_alpha(self.alpha)
        screen.blit(img_copy,(draw_x,draw_y))