import sys

import pygame
import utils.config as config
import scenes.game_scene as scene
import game_objects.role as role
import game_objects.weapon as weapon

# 刷新屏幕
def update_screen(bg,player,bullets,enemys,screen):
    bg.blitme()
    for bullet in bullets.sprites():
        bullet.drawme()
    player.blitme()
    enemys.draw(screen)
    pygame.display.flip()  # 刷新

# 事件检测
def check_event(player, screen, bullets,bullet_cfg):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player.moving_right = True
            elif event.key == pygame.K_LEFT:
                player.moving_left = True
            elif event.key == pygame.K_SPACE:
                new_bullet = weapon.Bullet(player,screen, bullet_cfg)
                bullets.add(new_bullet)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                player.moving_right = False
            elif event.key == pygame.K_LEFT:
                player.moving_left = False

# 创建敌人
def create_enemys(screen,enemys,enemy_cfg):
    enemy = role.Enemy(screen, enemy_cfg)
    enemys.add(enemy)
    number_enemys = screen.get_rect().width / (20 + enemy.rect.width)  # 利用屏幕总宽度除以单个敌人所占空间得出一行最大敌人数
    for index in range(int(number_enemys)):
        if index == 0:
            continue  # 终止当前循环，继续下次循环
        x = 10 + index * (20 + enemy.rect.width)  # 敌人之间存在10像素间隔
        new_enemy = role.Enemy(screen, enemy_cfg)
        new_enemy.rect.x = x
        enemys.add(new_enemy)

def update_enemys(enemys,bullets,enemy_cfg):
    enemys.update()
    # 检测碰撞
    hits = pygame.sprite.groupcollide(bullets, enemys, True, True)  # True表示碰撞后销毁
    for hit in hits:
        # 在碰撞位置创建爆炸效果
        explosion = weapon.Explosion(hit.rect.centerx, hit.rect.centery,enemy_cfg)
        enemys.add(explosion)  # 将爆炸精灵添加到所有精灵组中
    enemys.update()

def update_bullets(bullets):
    bullets.update()
    for bullet in bullets.sprites():  # 检测子弹是否超出屏幕外,控制子弹删除
        if bullet.rect.bottom < 0:
            bullets.remove(bullets)

def run():
    # 初始化pygame包
    pygame.init()
    # 加载配置
    cfg = config.read_yaml_config("config.yml")
    if cfg is None:
        print("Config file not found.")
        sys.exit(0)
    # 校验窗口配置
    screen_width = cfg.get('screen', {}).get('width', 0)
    screen_height = cfg.get('screen', {}).get('height', 0)
    screen_bg_src = cfg.get('screen', {}).get('bg_src', "")
    if screen_width == 0 | screen_height == 0 | screen_bg_src == "":
        print("Screen config not supported.")
        sys.exit(0)

    # 校验玩家配置
    player_cfg = cfg.get('player', {})
    if player_cfg is None:
        print("Player config not found.")
        sys.exit(0)
    # 校验敌人配置
    enemy_cfg = cfg.get('enemy', {})
    if enemy_cfg is None:
        print("Enemy config not found.")
        sys.exit(0)
    # 校验子弹配置
    bullet_cfg = cfg.get('bullet', {})
    if bullet_cfg is None:
        print("Bullet config not found.")
        sys.exit(0)
    # 初始化窗口
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()  # 创建一个Clock对象来控制帧率

    bg = scene.Bg(screen,screen_bg_src)

    player = role.Player(screen, player_cfg)
    # 初始化敌人

    enemys = pygame.sprite.Group()  # 管理敌人
    create_enemys(screen,enemys, enemy_cfg)

    bullets = pygame.sprite.Group()

    cnt = 0
    while True:
        # 每秒生成一次敌人
        if cnt % 200 == 0 :
            create_enemys(screen, enemys, enemy_cfg)

        check_event(player, screen, bullets, bullet_cfg)
        player.update()
        update_bullets(bullets)
        update_enemys(enemys,bullets,enemy_cfg)
        update_screen(bg,player,bullets,enemys,screen)
        # 控制帧率
        clock.tick(60)
        cnt += 1

run()



