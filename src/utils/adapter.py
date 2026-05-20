class ScreenAdapter:
    def __init__(self,screen_width,screen_height):
        self.width=screen_width
        self.height=screen_height
    def h_percent(self,percent):
        return int(self.height*percent/100)
    def w_percent(self,percent):
        return int(self.width*percent/100)    
        