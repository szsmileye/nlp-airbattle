import pygame


class Player:
    def __init__(self,screen,cfg):
        self.screen = screen
        self.image = pygame.image.load(cfg.get('image_path', ""))
        self.rect = self.image.get_rect()
        self.speed = cfg.get('speed', 1)
        # 计算玩家初始位置
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.moving_right = False
        self.moving_left = False
        self.centerx = self.screen_rect.centerx
    def blitme(self):
        self.screen.blit(self.image, self.rect)
    def update(self):
        # 判断向右移动且当前在屏幕内则移动
        if self.moving_right and self.rect.right < self.screen_rect.right :
            self.rect.centerx += self.speed
        # 判断向左移动且在屏幕内则移动
        if self.moving_left and self.rect.left > 0 :
            self.rect.centerx -= self.speed
        pass


class Enemy(pygame.sprite.Sprite):
    def __init__(self,screen,cfg):
        super(Enemy, self).__init__()
        self.screen = screen
        self.image = pygame.image.load(cfg.get('image_path', ""))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.speed = cfg.get('speed', 1)
        self.y = self.rect.y
        self.cnt = 1
    def blitme(self):
        self.screen.blit(self.image, self.rect)
    def update(self):
        self.y += self.speed
        self.rect.y = self.y
        if self.y > self.screen_rect.bottom :
            self.cnt = 0

