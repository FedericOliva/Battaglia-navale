import pygame
import math

class Button():
    def __init__(self, x, y, image) :
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked=False
        

    def drawWithBorder(self,screen):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == True  and self.clicked==False:
                self.clicked=True
                action=True

        if pygame.mouse.get_pressed()[0] == False:
            self.clicked=False  
        screen.blit(self.image,(self.rect.x, self.rect.y))
        pygame.draw.rect(screen,(0,0,0),self.rect,2)
        
        return action

def draw_text(text,font,text_color,x,y,screen):
    img = font.render(text, True, text_color)
    screen.blit(img, (x,y))

class box():
    def __init__(self,x,y,size):
        self.rect=pygame.Rect(0, 0, size, size)
        self.rect.topleft = (x,y)
        self.size=size
        self.xy=(x,y)

    def draw(self,screen):
        pos=pygame.mouse.get_pos()
        p=Point(self,self.rect.center)
        if self.rect.collidepoint(pos):
            pass
        p.map(screen)
        pygame.draw.rect(screen,(0,0,0),self.rect,2)
    

class nave():
    def __init__(self,x,y,image,campo):
        self.xy=(x,y)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        
        self.clicked=False
        self.movable=True
        self.selected=False
        self.sizex=self.rect.size[0]
        self.sizey=self.rect.size[1]
        self.surface=pygame.Surface((self.sizex, self.sizey))
        self.surface.blit(self.image,(0,0))
        self.boxes=self.calcHitBox()
        self.campo=campo
        self.center=self.rect.center
    
    def draw(self,screen,inGame):
        pos=pygame.mouse.get_pos()
        
        if not inGame:
            self.movable=False     
        if self.rect.collidepoint(pos) and self.movable:
            if pygame.mouse.get_pressed()[0] == True and self.clicked==False:
                self.selected=not self.selected
                self.clicked=True
                
        if self.selected:
            self.rect.center=pos
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r: 
                        self.rotate()
                        
        if pygame.mouse.get_pressed()[0] == False:
            self.clicked=False  
        screen.blit(self.image,(self.rect.x, self.rect.y))
        if(self.inPosition()==self.boxes):
            return True
        
    def rotate(self):
        self.image = pygame.transform.rotate(self.image,90)
        self.rect=self.image.get_rect()

    
    def inPosition(self):
        cont=0
        for colum in self.campo:
            for row in colum:
                if(self.rect.colliderect(row)):
                    cont+=1
        return cont
            
    def calcHitBox(self):
        if(self.sizex>self.sizey):return math.ceil(self.sizex/60)
        else:return math.ceil(self.sizey/60)
            

class Point():
    def __init__(self,rect,center):
        self.rect=rect
        self.point=pygame.Rect(0, 0, 50, 50)
        self.point.center=center

    def map(self,screen):
        pygame.draw.rect(screen,(0,0,0),self.point,2)
