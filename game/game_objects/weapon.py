import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self,player,screen,cfg):
        super(Bullet, self).__init__()  # 初始化父类
        self.screen = screen
        self.image = pygame.image.load(cfg.get('image_path', ""))
        self.rect = self.image.get_rect()
        self.rect.centerx = player.rect.centerx  # 子弹与飞机中心保持一致
        self.rect.y = player.rect.y  # y坐标也保持一致
        self.y = float(player.rect.y)  # 减小误差
        self.screen_rect = screen.get_rect()
        self.speed = cfg.get('speed', 1)
        self.color = (0,0,128)

    def update(self):
        self.y -= self.speed
        self.rect.y = self.y
    def drawme(self):  # 绘制方法
        # pygame.draw.rect(self.screen,self.color,self.rect)#绘制一个矩形上去 屏幕 颜色 位置及大小
        self.screen.blit(self.image, self.rect)


# 爆炸类
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y,cfg):
        super().__init__()
        # 加载爆炸图像（这里假设是一个单帧图像，实际中可以是动画）
        self.image = pygame.image.load(cfg.get('image_destory_path', "")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.lifetime = 500  # 爆炸效果的持续时间（帧数）
        self.age = 0

    def update(self):
        self.age += 1
        if self.age >= self.lifetime:
            self.kill()  # 爆炸结束后销毁精灵

