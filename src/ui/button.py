import pygame
class Button:
    def __init__(self,x,y,width,height,text="",
    color=(100,100,200),
    hover_color=(150,150,255,0),
    click_color=(80, 80, 180,0), 
    text_color=(255, 255, 255,0),
    font_size=40, border_radius=8
    ,icon_type='text'):
        self.rect = pygame.Rect(x, y, width, height)
        self.width=width
        self.height=height
        self.text=text
        self.color=color
        self.hover_color=hover_color
        self.click_color=click_color
        self.text_color=text_color
        self.font_size=font_size
        self.border_radius=border_radius
        self.font=pygame.font.SysFont(None,self.font_size)
        self.is_hovered=False
        self.on_click = None
        self.on_hover = None
        self.on_release = None
        self.is_clicked=False
        self.icon_type=icon_type
        self.surface=None
    def handle_events(self,event,offset_x=0,offset_y=0):
        if event.type not in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
            return
        event_pos_x,event_pos_y=event.pos
        event_pos_x-=offset_x
        event_pos_y-=offset_y
        if event.type==pygame.MOUSEMOTION:
            previous_hover=self.is_hovered
            self.is_hovered=self.rect.collidepoint(event_pos_x,event_pos_y)
            if self.is_hovered and not previous_hover and self.on_hover:
                self.on_hover()
        elif event.type==pygame.MOUSEBUTTONDOWN:
            if event.button==1:
                if self.rect.collidepoint(event_pos_x,event_pos_y) :
                    self.is_clicked=True 
                    if self.on_click :
                        self.on_click()  
        elif event.type==pygame.MOUSEBUTTONUP:
            if event.button==1:
                if self.is_clicked and self.rect.collidepoint(event_pos_x,event_pos_y):
                    if self.on_release:
                        self.on_release()
                self.is_clicked=False
 
    def draw(self,surface):
        self.surface=surface
        if self.is_clicked:
            current_color=self.click_color
        elif self.is_hovered:
            current_color = self.hover_color
        else:
            current_color = self.color
        pygame.draw.rect(self.surface,current_color,self.rect,border_radius=self.border_radius)
        pygame.draw.rect(self.surface,(50,50,50),self.rect,2,self.border_radius)
        
            
        if self.text:
            text_surface=self.font.render(self.text,True,self.text_color)
            text_surface_rect=text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface,text_surface_rect)
    def draw_polygen(self):
        pygame.draw.polygon(self.surface,self.text_color,[(25,7),(25,93),(100,50)])
    def draw_line(self):
        pygame.draw.line(self.surface,self.text_color,(30,30),(30,70))
        pygame.draw.line(self.surface,self.text_color,(70,30),(70,70))
    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y
    
    def set_size(self, width, height):
        self.rect.width = width
        self.rect.height = height
    
    def set_text(self, text):
        self.text = text
    
    def  set_callbacks(self,on_click=None,on_hover=None, on_release=None):
        self.on_click = on_click
        self.on_hover = on_hover
        self.on_release = on_release  