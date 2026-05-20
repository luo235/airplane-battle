import pygame
import math
class JoyStick:
    def __init__(self,screen,base_pos=(100,200),base_r=160,knob_r=80,
    base_color=(140,140,140,150),knob_color=(255,255,255,150),line_width=1):
        self.base_x,self.base_y=base_pos
        self.screen=screen
        self.base_r=base_r
        self.knob_r=knob_r
        self.base_color=base_color
        self.knob_color=knob_color
        self.line_width=line_width
        self.knob_x,self.knob_y=base_pos
        self.is_cliked=False
        self.dx=0
        self.dy=0
    def handle_events(self,event):
        if event.type==pygame.MOUSEBUTTONDOWN:
            x,y=event.pos
            dx=x-self.base_x
            dy=y-self.base_y
            if math.hypot(dx,dy)<=self.knob_r:
                self.is_cliked=True
                self.dx=dx
                self.dy=dy
        elif event.type==pygame.MOUSEMOTION:
            if self.is_cliked:
               x,y=event.pos
               dx=x-self.base_x
               dy=y-self.base_y 
               if math.hypot(dx,dy)>self.knob_r:
                  rad=math.atan2(dy,dx)
                  self.dx=self.knob_r*math.cos(rad)
                  self.dy=self.knob_r*math.sin(rad)
               else :
                   self.dx=dx
                   self.dy=dy
        elif event.type==pygame.MOUSEBUTTONUP:
            self.dx=0
            self.dy=0
            self.is_cliked=False
        
    def draw(self):
        base_surface = pygame.Surface((self.base_r*2, self.base_r*2),pygame.SRCALPHA)
        pygame.draw.circle(base_surface,self.base_color,(self.base_r,self.base_r),self.base_r)
        pygame.draw.circle(base_surface,self.knob_color,(self.base_r+self.dx,self.base_r+self.dy),self.knob_r)
        self.screen.blit(base_surface,(self.base_x-self.base_r,self.base_y-self.base_r))
        