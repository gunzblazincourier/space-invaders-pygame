import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

PLAYER_WIDTH = 13
PLAYER_HEIGHT = 7

BULLET_WIDTH = 1
BULLET_HEIGHT = 4
bullet_shot = False

spritesheet = pygame.image.load('sheet.png').convert()
player = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT)).convert()
player.blit(spritesheet, (0, 0), (3, 49, PLAYER_WIDTH, PLAYER_HEIGHT))
player = pygame.transform.scale_by(player, 5)
player_position = pygame.Vector2(640, 600)
gun_position = pygame.Vector2(672, 600)

bullet = pygame.Surface((BULLET_WIDTH, BULLET_HEIGHT)).convert()
bullet.blit(spritesheet, (0, 0), (55, 53, BULLET_WIDTH, BULLET_HEIGHT))
bullet = pygame.transform.scale_by(bullet, 2)
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
    if keys[pygame.K_LEFT]:
        player_position.x -= 300 * dt
        gun_position.x -= 300 * dt
    elif keys[pygame.K_RIGHT]:
        player_position.x += 300 * dt
        gun_position.x += 300 * dt

    if bullet_position.y < 0:
        bullet_shot = False
        bullet_position = gun_position

    if bullet_shot == True:
        bullet_position.y -= 500 * dt

    screen.fill((0, 0, 0))
    screen.blit(player, (player_position.x, player_position.y))
    screen.blit(bullet, (bullet_position.x, bullet_position.y))
    pygame.display.flip()

pygame.quit()
