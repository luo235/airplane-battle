import pygame
class Sheet:
    @staticmethod
    def load_sprite_sheet(path,width,height,scale=None):
        sheet=pygame.image.load(path).convert_alpha()
        frames=[]
        for x in range(0,sheet.get_height(),height):
            for y in range(0,sheet.get_width(),width):
                frame=sheet.subsurface(y,x,width,height)
                if scale:
                    frame=pygame.transform.scale(frame,scale)
                frames.append(frame)
        return frames