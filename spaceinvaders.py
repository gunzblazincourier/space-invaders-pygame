import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

PLAYER_WIDTH = 13
PLAYER_HEIGHT = 7

BULLET_WIDTH = 1
BULLET_HEIGHT = 4


spritesheet = pygame.image.load('sheet.png').convert()
player = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT)).convert()
player.blit(spritesheet, (0, 0), (3, 49, PLAYER_WIDTH, PLAYER_HEIGHT))
player = pygame.transform.scale_by(player, 7)
player_pos = pygame.Vector2(640, 600)
gun = pygame.Vector2(646, 600)

bullet = pygame.Surface((BULLET_WIDTH, BULLET_HEIGHT)).convert()
bullet.blit(spritesheet, (0, 0), (55, 53, BULLET_WIDTH, BULLET_HEIGHT))
bullet = pygame.transform.scale_by(bullet, 7)
bullet_pos = pygame.Vector2(640, 500)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos.x -= 300 * dt
        gun.x -= 300 * dt
    elif keys[pygame.K_RIGHT]:
        player_pos.x += 300 * dt
        gun.x += 300 * dt

    screen.fill((0, 0, 0))
    screen.blit(player, (player_pos.x, player_pos.y))
    screen.blit(bullet, (bullet_pos.x, bullet_pos.y))
    pygame.display.flip()
    dt = clock.tick(144) / 1000

pygame.quit()
