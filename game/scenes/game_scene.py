import pygame
class Bg:  # 定义一个背景类
    def __init__(self ,screen, img_src):
        self.screen = screen
        self.image = pygame.image.load(img_src)
        self.rect = self.image.get_rect()

    def blitme(self)  :  # 绘制自身
        self.screen.blit(self.image ,self.rect)