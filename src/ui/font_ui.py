import pygame.font
class Font_ui :
    def __init__(self,game_ctx,font_text,font_size=72):
        self.screen=game_ctx.screen
        self.screen_rect=self.screen.get_rect()
        self.settings=game_ctx.settings
        self.text_color=(30,30,30)
        self.font_size=font_size
        self.font=pygame.font.SysFont(None,self.font_size)
        self.text = font_text
    def prep_font(self,start=100) :
        if isinstance(self.text,list):
            texts=self.text
        else :
            texts=[self.text]    
        for i,text in enumerate(texts):    
            img=self.font.render(text,True,self.text_color,self.settings.bg_color)     
            img_rect=img.get_rect()
            img_rect.centerx=self.screen_rect.centerx
            img_rect.y=start+100*i
            self.screen.blit(img,img_rect)