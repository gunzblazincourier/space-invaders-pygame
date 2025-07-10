import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
spritesheet = pygame.image.load('sheet.png')
player = pygame.Surface((14, 7))
player.blit(spritesheet, (0, 0), (2, 49, 14, 7))
player = pygame.transform.scale_by(player, 3)
player_pos = pygame.Vector2(640, 600)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos.x -= 300 * dt
    elif keys[pygame.K_RIGHT]:
        player_pos.x += 300 * dt

    screen.fill((0, 0, 0))
    screen.blit(player, (player_pos.x, player_pos.y))
    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
