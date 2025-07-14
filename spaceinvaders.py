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

enemy_direction = True  #True = right; False = left
previous_second = 0
current_second = 0

ENEMY_ROWS, ENEMY_COLUMNS = (5, 11)
enemy_positions_list =  [[player_position for _ in range(ENEMY_COLUMNS)] for _ in range(ENEMY_ROWS)]
enemy_check_list = [[False for _ in range(ENEMY_COLUMNS)] for _ in range(ENEMY_ROWS)]
enemy_timer_list = [[1.00 for _ in range(ENEMY_COLUMNS)] for _ in range(ENEMY_ROWS)]
enemy_position_x = 40
enemy_position_y = 60
for i in range(ENEMY_ROWS):
    for j in range(ENEMY_COLUMNS):
        enemy_positions_list[i][j] = pygame.Vector2(enemy_position_x, enemy_position_y)
        enemy_position_x += 16
    enemy_position_x = 40
    enemy_position_y += 15
print(enemy_positions_list)

ENEMY_WIDTH = 16
ENEMY_HEIGHT = 8
enemy_list = [[player for _ in range(ENEMY_COLUMNS)] for _ in range(ENEMY_ROWS)]
for i in range(ENEMY_ROWS):
    for j in range(ENEMY_COLUMNS):
        enemy = pygame.Surface((ENEMY_WIDTH, ENEMY_HEIGHT)).convert()
        enemy_list[i][j] = enemy
print(enemy_list)

BULLET_WIDTH = 1
BULLET_HEIGHT = 4
bullet = pygame.Surface((BULLET_WIDTH, BULLET_HEIGHT)).convert()
bullet.blit(spritesheet, (0, 0), (55, 53, BULLET_WIDTH, BULLET_HEIGHT))
gun_position = pygame.Vector2(136, 200)
bullet_position = gun_position

sound_shoot = pygame.mixer.Sound('shoot.wav')
channel_shoot = pygame.mixer.Channel(1)

linebreak_list = []
bullet_shot = False
running = True
while running:
    dt = clock.tick(144) / 1000
    current_second = int(pygame.time.get_ticks() / 1000)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and bullet_shot == False:
        bullet_position = pygame.Vector2(gun_position.x, gun_position.y)
        bullet_shot = True
        channel_shoot.play(sound_shoot)
    if keys[pygame.K_LEFT] and player_position.x > 30:
        player_position.x -= 100 * dt
        gun_position.x -= 100 * dt
    elif keys[pygame.K_RIGHT] and player_position.x < 220:
        player_position.x += 100 * dt
        gun_position.x += 100 * dt

    if bullet_position.y < 15:
        bullet_shot = False
        linebreak_list.append(int(bullet_position.x))

    if bullet_shot:
        bullet_position.y -= 200 * dt
    else:
        bullet_position = gun_position

    for i in range(ENEMY_ROWS):
        for j in range(ENEMY_COLUMNS):
            if enemy_check_list[i][j]:
                if enemy_timer_list[i][j] > 0:
                    enemy_timer_list[i][j] -= 5 * dt
                    enemy_list[i][j].blit(spritesheet, (0, 0), (55, 1, ENEMY_WIDTH, ENEMY_HEIGHT))
                else:
                    enemy_timer_list[i][j] = 0
            else:
                if previous_second != current_second:
                    if enemy_direction:
                        if enemy_positions_list[ENEMY_ROWS-1][ENEMY_COLUMNS-1].x < 220:
                            enemy_positions_list[i][j].x += 3
                        else:
                            print("yes")
                            enemy_positions_list[i][j].y += 3
                            if (i == ENEMY_ROWS-1) and (j == ENEMY_COLUMNS-1):
                                enemy_direction = False
                    else:
                        #print(enemy_positions_list[0][ENEMY_ROWS-1])
                        if enemy_positions_list[ENEMY_ROWS-1][ENEMY_COLUMNS-1].x > 185:
                            enemy_positions_list[i][j].x -= 3
                        else:
                            print("yes")
                            enemy_positions_list[i][j].y += 3
                            if (i == ENEMY_ROWS-1) and (j == ENEMY_COLUMNS-1):
                                enemy_direction = True

                if i == 0:
                    if current_second % 2 == 0:
                        enemy_list[i][j].blit(spritesheet, (0, 0), (1, 1, ENEMY_WIDTH, ENEMY_HEIGHT))
                    elif current_second % 2 == 1:
                        enemy_list[i][j].blit(spritesheet, (0, 0), (1, 11, ENEMY_WIDTH, ENEMY_HEIGHT))
                elif i == 1 or i == 2:
                    if current_second % 2 == 0:
                        enemy_list[i][j].blit(spritesheet, (0, 0), (19, 1, ENEMY_WIDTH, ENEMY_HEIGHT))
                    elif current_second % 2 == 1:
                        enemy_list[i][j].blit(spritesheet, (0, 0), (19, 11, ENEMY_WIDTH, ENEMY_HEIGHT))
                else:
                    if current_second % 2 == 0:
                        enemy_list[i][j].blit(spritesheet, (0, 0), (37, 1, ENEMY_WIDTH, ENEMY_HEIGHT))
                    elif current_second % 2 == 1:
                        enemy_list[i][j].blit(spritesheet, (0, 0), (37, 11, ENEMY_WIDTH, ENEMY_HEIGHT))
    previous_second = current_second
    # if enemy_positions_list[ENEMY_ROWS-1][ENEMY_COLUMNS-1].x >= 220 or enemy_positions_list[ENEMY_ROWS-1][ENEMY_COLUMNS-1].x <= 190:
    #     if enemy_direction:
    #         enemy_direction = False
    #     else:
    #         enemy_direction = True

    SCREEN.fill((0, 0, 0))
    SCREEN.blit(player, (player_position.x, player_position.y))
    for i in range(ENEMY_ROWS):
        for j in range(ENEMY_COLUMNS):
            if bullet_shot == True and enemy_check_list[i][j] == False:
                if (enemy_positions_list[i][j].x + 3 < bullet_position.x <
                        enemy_positions_list[i][j].x + ENEMY_WIDTH - 3) and \
                        bullet_position.y < enemy_positions_list[i][j].y + ENEMY_HEIGHT:
                    enemy_check_list[i][j] = True
                    bullet_shot = False
            if enemy_timer_list[i][j] > 0:
                SCREEN.blit(enemy_list[i][j], (enemy_positions_list[i][j].x, enemy_positions_list[i][j].y))
    SCREEN.blit(bullet, (bullet_position.x, bullet_position.y))

    for i in range(28, 230):
        if i in linebreak_list:
            continue
        #pygame.draw.line(SCREEN, (255, 255, 255), (i, 15), (i, 15))
        SCREEN.set_at((i, 15), (255, 255, 255))
    pygame.display.flip()

pygame.quit()
