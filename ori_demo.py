import sys#退出程序
import pygame

class Settings():
     def __init__(self):
          self.screen_width=480
          self.screen_height=852
          self.bg_color = (255,192,203)
          self.hero_speed = 2#控制飞机移速
             
          self.bullet_speed = 4
          self.bullet_width = 4
          self.bullet_height = 8
          self.bullet_color = (0,0,128)#设置子弹属性
          self.enemy_speed = 1

class Enemy(pygame.sprite.Sprite):#创建敌人类
     def __init__(self,screen,settings):
          super(Enemy,self).__init__()
          self.screen = screen
          self.settings = settings
          self.image = pygame.image.load("assets/images/enemy1.png")
          self.rect = self.image.get_rect()
          self.rect.x = 10
          self.rect.y = 10
          self.speed = settings.enemy_speed
          self.y = float(self.rect.y)

     def update(self):
          self.y += self.speed
          self.rect.y = self.y
        
     def blitme(self):#绘制
          self.screen.blit(self.image,self.rect)          
             
class Bullet(pygame.sprite.Sprite):#继承sprite 精灵
     def __init__(self,screen,settings,hero):
          super(Bullet,self).__init__()#初始化父类
          self.screen = screen
          self.settings = settings

          self.image = pygame.image.load('assets/images/bullet1.png')#图片绘制子弹
          self.rect = self.image.get_rect()
          #self.rect = pygame.Rect(0,0,settings.bullet_width,settings.bullet_height)
          self.rect.centerx = hero.rect.centerx#子弹与飞机中心保持一致
          self.rect.y =hero.rect.y#y坐标也保持一致
          self.y = float(hero.rect.y)#减小误差
          self.speed = settings.bullet_speed#把自身速度保存下来
          self.color = settings.bullet_color

     def update(self):#子弹移动 子弹持续向上移动 让y坐标减少即可
          self.y -= self.speed
          self.rect.y = self.y

     def drawme(self):#绘制方法
          #pygame.draw.rect(self.screen,self.color,self.rect)#绘制一个矩形上去 屏幕 颜色 位置及大小
          self.screen.blit(self.image,self.rect)

class Bg():#定义一个背景类
     def __init__(self,screen):
          self.screen = screen
          self.image = pygame.image.load("assets/images/background.png")
          self.rect = self.image.get_rect()

     def blitme(self):#绘制自身
          self.screen.blit(self.image,self.rect)

class Hero():#绘制飞机
     def __init__(self,screen,settings):
          self.screen = screen
          self.settings = settings#控制飞机移速
          self.image = pygame.image.load("assets/images/player1.png")
          self.rect = self.image.get_rect()
          self.screen_rect = screen.get_rect()
          #self.rect.x = self.screen_rect.width/2 - self.rect.width/2#保证居中，屏幕宽度一半减去自身宽度一半
          self.rect.centerx = self.screen_rect.centerx#利用中心点坐标
          self.rect.bottom = self.screen_rect.bottom#botom自身高度，位于最下方
          self.moving_right = False#设置一个标志位，控制按键按下与抬起
          self.moving_left = False
          self.centerx = float(self.screen_rect.centerx)#修改误差，不让它忽略小数
             
     def blitme(self):#绘制自身
          self.screen.blit(self.image,self.rect)

     def update(self):#控制飞机移动
          if self.moving_right and self.rect.right < self.screen_rect.right:#控制飞机右边不能超出屏幕边界
               self.centerx += self.settings.hero_speed
          if self.moving_left and self.rect.left > 0:#控制到左边距离大于0
               self.centerx -= self.settings.hero_speed
          self.rect.centerx = self.centerx

def check_events(screen,settings,hero,bullets):#事件检测
     for event in pygame.event.get():
          if event.type == pygame.QUIT:
               pygame.quit()
               sys.exit()
          elif event.type == pygame.KEYDOWN:#判断是否按键按下
               if event.key == pygame.K_RIGHT:#判断是否按下方向右键
                    hero.moving_right = True
               elif event.key == pygame.K_LEFT:
                    hero.moving_left = True
               elif event.key == pygame.K_SPACE:
                    new_bullet = Bullet(screen,settings,hero)
                    bullets.add(new_bullet)               
          elif event.type == pygame.KEYUP:
               if event.key == pygame.K_RIGHT:
                    hero.moving_right = False
               elif event.key == pygame.K_LEFT:
                    hero.moving_left = False

def update_screen(bg,hero,bullets,enemys,screen):
     bg.blitme()
     for bullet in bullets.sprites():
          bullet.drawme()
     hero.blitme()
     #enemy.blitme()
     enemys.draw(screen)
     pygame.display.flip()#刷新

def update_bullets(bullets):
     bullets.update()
     for bullet in bullets.sprites():#检测子弹是否超出屏幕外,控制子弹删除
          if bullet.rect.bottom<0:
               bullets.remove(bullets)

def update_enemys(enemys,bullets):
     enemys.update()
     pygame.sprite.groupcollide(bullets,enemys,True,True)#组的碰撞检测，传递两个组，True代表碰撞后是否销毁

def create_enemys(enemys,screen,settings):#控制多个敌人生成
     enemy = Enemy(screen,settings)
     enemys.add(enemy)
     number_enemys = screen.get_rect().width/(20+enemy.rect.width)#利用屏幕总宽度除以单个敌人所占空间得出一行最大敌人数
     for index in range(int(number_enemys)):
          if index==0:
               continue#终止当前循环，继续下次循环
          x = 10 + index * (20+enemy.rect.width)#敌人之间存在10像素间隔
          new_enemy = Enemy(screen,settings)
          new_enemy.rect.x = x
          enemys.add(new_enemy)

def run_game():
     pygame.init()#创建可视化窗口5    
     settings = Settings()
     screen = pygame.display.set_mode((settings.screen_width,settings.screen_height))#设置窗口大小
     bg = Bg(screen)
     hero = Hero(screen,settings)
     #enemy = Enemy(screen,settings)
     bullets = pygame.sprite.Group()#管理子弹
     enemys = pygame.sprite.Group()#管理敌人
     create_enemys(enemys,screen,settings)
        
     while True:     
          check_events(screen,settings,hero,bullets)
          hero.update()
          update_bullets(bullets)
          update_enemys(enemys,bullets)
          #print(len(bullets.sprites()))#验证删除子弹代码是否生效
          update_screen(bg,hero,bullets,enemys,screen)
             

run_game()    