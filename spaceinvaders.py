import pygame

pygame.init()
SCREEN = pygame.display.set_mode((256, 224), pygame.SCALED | pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True

PLAYER_WIDTH = 13
PLAYER_HEIGHT = 7

BULLET_WIDTH = 1
BULLET_HEIGHT = 4
bullet_shot = False

linebreak_list = []

spritesheet = pygame.image.load('sheet.png').convert()
player = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT)).convert()
player.blit(spritesheet, (0, 0), (3, 49, PLAYER_WIDTH, PLAYER_HEIGHT))
player_position = pygame.Vector2(128, 185)
gun_position = pygame.Vector2(134, 185)

bullet = pygame.Surface((BULLET_WIDTH, BULLET_HEIGHT)).convert()
bullet.blit(spritesheet, (0, 0), (55, 53, BULLET_WIDTH, BULLET_HEIGHT))
bullet_position = gun_position

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

    if bullet_shot == True:
        bullet_position.y -= 200 * dt

    SCREEN.fill((0, 0, 0))
    SCREEN.blit(player, (player_position.x, player_position.y))
    SCREEN.blit(bullet, (bullet_position.x, bullet_position.y))

    for i in range(28, 230):
        if i in linebreak_list:
            continue
        pygame.draw.line(SCREEN, (255, 255, 255), (i, 15), (i, 15))
    #pygame.draw.line(SCREEN, (255, 255, 255), (30, 210), (220, 210))
    pygame.display.flip()

pygame.quit()
