import pygame

pygame.init()
SCREEN = pygame.display.set_mode((256, 224), pygame.SCALED | pygame.FULLSCREEN)
clock = pygame.time.Clock()
spritesheet = pygame.image.load('sheet.png').convert()

PLAYER_WIDTH = 16
PLAYER_HEIGHT = 8
player = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT)).convert()
player.blit(spritesheet, (0, 0), (1, 49, PLAYER_WIDTH, PLAYER_HEIGHT))
player_position = pygame.Vector2(128, 200)

enemy_rows, enemy_columns = (11, 5)
enemy_positions_list =  [[player_position for i in range(enemy_columns)] for j in range(enemy_rows)]
enemy_position_x = 50
enemy_position_y = 70
for i in range(enemy_columns):
    for j in range(enemy_rows):
        enemy_positions_list[j][i] = pygame.Vector2(enemy_position_x, enemy_position_y)
        enemy_position_x += 14
    enemy_position_x = 50
    enemy_position_y += 10
print(enemy_positions_list)

ENEMY_WIDTH = 16
ENEMY_HEIGHT = 8
enemy_list = [[player for i in range(enemy_columns)] for j in range(enemy_rows)]
for i in range(enemy_columns):
    for j in range(enemy_rows):
        enemy = pygame.Surface((ENEMY_WIDTH, ENEMY_HEIGHT)).convert()
        enemy_list[j][i] = enemy
print(enemy_list)

BULLET_WIDTH = 1
BULLET_HEIGHT = 4
bullet = pygame.Surface((BULLET_WIDTH, BULLET_HEIGHT)).convert()
bullet.blit(spritesheet, (0, 0), (55, 53, BULLET_WIDTH, BULLET_HEIGHT))
gun_position = pygame.Vector2(136, 200)
bullet_position = gun_position

linebreak_list = []
bullet_shot = False
running = True
while running:
    dt = clock.tick(144) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and bullet_shot == False:
        bullet_position = pygame.Vector2(gun_position.x, gun_position.y)
        bullet_shot = True
    if keys[pygame.K_LEFT] and player_position.x > 30:
        player_position.x -= 100 * dt
        gun_position.x -= 100 * dt
    elif keys[pygame.K_RIGHT] and player_position.x < 220:
        player_position.x += 100 * dt
        gun_position.x += 100 * dt

    if bullet_position.y < 15:
        bullet_shot = False
        linebreak_list.append(int(bullet_position.x))
        bullet_position = gun_position

    if bullet_shot:
        bullet_position.y -= 200 * dt

    for i in range(enemy_columns):
        for j in range(enemy_rows):
            if int(pygame.time.get_ticks() / 1000) % 2 == 0:
                enemy_list[j][i].blit(spritesheet, (0, 0), (1, 1, ENEMY_WIDTH, ENEMY_HEIGHT))
            elif int(pygame.time.get_ticks() / 1000) % 2 == 1:
                enemy_list[j][i].blit(spritesheet, (0, 0), (1, enemy_rows, ENEMY_WIDTH, ENEMY_HEIGHT))
    SCREEN.fill((0, 0, 0))
    SCREEN.blit(player, (player_position.x, player_position.y))
    for i in range(enemy_columns):
        for j in range(enemy_rows):
            SCREEN.blit(enemy_list[j][i], (enemy_positions_list[j][i].x, enemy_positions_list[j][i].y))
    SCREEN.blit(bullet, (bullet_position.x, bullet_position.y))

    for i in range(28, 230):
        if i in linebreak_list:
            continue
        #pygame.draw.line(SCREEN, (255, 255, 255), (i, 15), (i, 15))
        SCREEN.set_at((i, 15), (255, 255, 255))
    pygame.display.flip()

pygame.quit()
