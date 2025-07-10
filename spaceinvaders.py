import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
spritesheet = pygame.image.load('sheet.png')
player = pygame.Surface((14, 7))
player.blit(spritesheet, (0, 0), (2, 49, 14, 7))
player = pygame.transform.scale_by(player, 3)
screen.blit(player, (640, 600))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
