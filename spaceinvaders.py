from fileinput import filename

import pygame
from pygame import Surface


def initialize_pygame_modules():
    pygame.init()

def initialize_display_window():
    return pygame.display.set_mode((256, 224), pygame.SCALED)

def create_surface(width, height):
    return pygame.Surface((width, height)).convert()

def load_image(filepath):
    return pygame.image.load(filepath).convert()

def draw_surface_on_surface(surface_top, surface_bottom, destination, area):
    return surface_bottom.blit(surface_top, destination, area)

def assign_coordinates(x, y):
    return pygame.Vector2(x, y)

def set_enemy_direction(direction):
    return direction

def set_enemy_list_dimensions(rows, columns):
    return rows, columns

def initialize_2d_list(value, rows, columns):
    return [[value for _ in range(columns)] for _ in range(rows)]


def assign_coordinates_to_positions_list(positions, rows, columns, x, y):
    for i in range(rows):
        for j in range(columns):
            positions[i][j] = assign_coordinates(x, y)
            x += 16
        x = 40
        y += 15
    return positions

def create_sound_object(filepath):
    return pygame.mixer.Sound(filepath)

def set_sound_channel(channel_number):
    return pygame.mixer.Channel(channel_number)

def create_clock():
    return pygame.time.Clock()

def set_fps(fps):
    return clock.tick(fps)

def set_delta_time(fps):
    return set_fps(fps) / 1000

def get_events_from_queue():
    return pygame.event.get()

def check_quit_event(event):
    if event.type == pygame.QUIT:
        return False
    return True

def get_all_keys_state():
    return pygame.key.get_pressed()

def check_key_press(keys, key):
    return keys[key]

def move_object_and_account_delta_time(object, speed, dt):
    object += speed * dt
    return object

def play_sound_from_channel(soundpath, channel):
    set_sound_channel(channel).play(create_sound_object(soundpath))

def add_item_in_front_of_list(l, item):
    l.append(item)
    return l

def fill_surface_with_color(surface, color):
    surface.fill(color)

def draw_coloured_pixel_on_surface(surface, position, color):
    surface.set_at(position, color)

def update_display_surface():
    pygame.display.flip()

def quit_game():
    pygame.quit()





#pygame.init()
#SCREEN = pygame.display.set_mode((256, 224), pygame.SCALED)

PLAYER_WIDTH = 16
PLAYER_HEIGHT = 8
player = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT)).convert()

spritesheet = pygame.image.load('sheet.png').convert()
player.blit(spritesheet, (0, 0), (1, 49, PLAYER_WIDTH, PLAYER_HEIGHT))
player_position = pygame.Vector2(128, 200)

enemy_direction = True  #True = right; False = left
previous_second = 0 #No function
current_second = 0  #No function
ENEMY_ROWS, ENEMY_COLUMNS = (5, 11)

# player_position assigned by default to set correct data type of Vector2 to values
enemy_positions_list =  [[player_position for _ in range(ENEMY_COLUMNS)] for _ in range(ENEMY_ROWS)]

# Stores which enemies are dead
enemy_death_list = [[False for _ in range(ENEMY_COLUMNS)] for _ in range(ENEMY_ROWS)]

# Dead enemies play death animation until timer runs out
enemy_timer_list = [[1.00 for _ in range(ENEMY_COLUMNS)] for _ in range(ENEMY_ROWS)]

# Helps assign positions to enemies by updating values in these variables during below loop
enemy_position_x = 40
enemy_position_y = 60
for i in range(ENEMY_ROWS):
    for j in range(ENEMY_COLUMNS):
        enemy_positions_list[i][j] = pygame.Vector2(enemy_position_x, enemy_position_y)
        enemy_position_x += 16
    enemy_position_x = 40
    enemy_position_y += 15

ENEMY_WIDTH = 16
ENEMY_HEIGHT = 8
enemy_list = [[player for _ in range(ENEMY_COLUMNS)] for _ in range(ENEMY_ROWS)]
for i in range(ENEMY_ROWS):
    for j in range(ENEMY_COLUMNS):
        enemy = pygame.Surface((ENEMY_WIDTH, ENEMY_HEIGHT)).convert()
        enemy_list[i][j] = enemy

BULLET_WIDTH = 1
BULLET_HEIGHT = 4
bullet = pygame.Surface((BULLET_WIDTH, BULLET_HEIGHT)).convert()
bullet.blit(spritesheet, (0, 0), (55, 53, BULLET_WIDTH, BULLET_HEIGHT))
gun_position = pygame.Vector2(136, 200)
bullet_position = gun_position  # 'Stores' bullet in gun of spaceship by default

sound_shoot = pygame.mixer.Sound('shoot.wav')
channel_shoot = pygame.mixer.Channel(1)

# Row and column of the last enemy in the list when traversed column-by-column instead of the normal row-by-row looping
# left-to-right list traversal for right travel direction, and right-to-left traversal for left direction
# (default is for bottom-rightmost enemy)
last_enemy_row = ENEMY_ROWS - 1
last_enemy_column = ENEMY_COLUMNS - 1
enemy_position_y = 0

linebreak_list = [] # Line is broken at which locations
bullet_shot = False
game_running = True
clock = pygame.time.Clock()
while game_running:
    delta_time = clock.tick(144) / 1000
    current_second = int(pygame.time.get_ticks() / 1000)    # No function

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and bullet_shot == False:
        bullet_position = pygame.Vector2(gun_position.x, gun_position.y)
        bullet_shot = True
        channel_shoot.play(sound_shoot)
    if keys[pygame.K_LEFT] and player_position.x > 30:
        player_position.x -= 100 * delta_time
        gun_position.x -= 100 * delta_time
    elif keys[pygame.K_RIGHT] and player_position.x < 220:
        player_position.x += 100 * delta_time
        gun_position.x += 100 * delta_time

    # Bullet destroys line where it hits
    if bullet_position.y < 15:
        bullet_shot = False
        linebreak_list.append(int(bullet_position.x))

    if bullet_shot:
        bullet_position.y -= 200 * delta_time
    else:
        bullet_position = gun_position  #  Bullet respawns at gun_position

    # Updates coordinates of the last enemy when an enemy is killed, based on the direction of travel
    # print(last_enemy_row, last_enemy_column)
    if enemy_direction:
        for j in range(ENEMY_COLUMNS):
            for i in range(ENEMY_ROWS):
                if not enemy_death_list[i][j]:
                    last_enemy_row = i
                    last_enemy_column = j
    else:
        for j in range(ENEMY_COLUMNS - 1, -1, -1):
            for i in range(ENEMY_ROWS):
                if not enemy_death_list[i][j]:
                    last_enemy_row = i
                    last_enemy_column = j

    if enemy_direction:
        for j in range(ENEMY_COLUMNS):
            for i in range(ENEMY_ROWS):
                if previous_second != current_second:  # Means if one second has passed
                    if enemy_positions_list[last_enemy_row][last_enemy_column].x < 210:
                        enemy_positions_list[i][j].x += 3
                    else:
                        print(enemy_position_y, enemy_positions_list[last_enemy_row][last_enemy_column].y)
                        if enemy_position_y != enemy_positions_list[last_enemy_row][last_enemy_column].y:
                            enemy_positions_list[i][j].x += 3
                            if (i == last_enemy_row) and (j == last_enemy_column):
                                enemy_position_y = enemy_positions_list[last_enemy_row][last_enemy_column].y
                        else:
                            enemy_positions_list[i][j].y += 3
                            enemy_position_y = enemy_positions_list[last_enemy_row][last_enemy_column].y
                            if (i == last_enemy_row) and (j == last_enemy_column):
                                enemy_direction = False
                                enemy_position_y -= 2
    else:
        for j in range(ENEMY_COLUMNS - 1, -1, -1):
            for i in range(ENEMY_ROWS):
                if previous_second != current_second:  # Means if one second has passed
                    if enemy_positions_list[last_enemy_row][last_enemy_column].x > 40:
                        enemy_positions_list[i][j].x -= 3
                    else:
                        print(enemy_position_y, enemy_positions_list[last_enemy_row][last_enemy_column].y)
                        if enemy_position_y != enemy_positions_list[last_enemy_row][last_enemy_column].y:
                            enemy_positions_list[i][j].x -= 3
                            if (i == last_enemy_row) and (j == last_enemy_column):
                                enemy_position_y = enemy_positions_list[last_enemy_row][last_enemy_column].y
                        else:
                            enemy_positions_list[i][j].y += 3
                            enemy_position_y = enemy_positions_list[last_enemy_row][last_enemy_column].y
                            if (i == last_enemy_row) and (j == last_enemy_column):
                                enemy_direction = True
                                enemy_position_y -= 2



    for i in range(ENEMY_ROWS):
        for j in range(ENEMY_COLUMNS):
            if enemy_death_list[i][j]:
                if enemy_timer_list[i][j] > 0:
                    enemy_timer_list[i][j] -= 5 * delta_time    # Play dead enemy's timer for death animation
                    enemy_list[i][j].blit(spritesheet, (0, 0), (55, 1, ENEMY_WIDTH, ENEMY_HEIGHT))
                else:
                    enemy_timer_list[i][j] = 0  # Death animation finished, enemy removed
            else:
            #     if previous_second != current_second: # Means if one second has passed
            #         if enemy_direction:
            #             if enemy_positions_list[last_enemy_row][last_enemy_column].x < 220:
            #                 enemy_positions_list[i][j].x += 3
            #             else:
            #                 if enemy_position_y != enemy_positions_list[last_enemy_row][last_enemy_column].y:
            #                     enemy_positions_list[i][j].x += 3
            #                     if (i == ENEMY_ROWS-1) and (j == ENEMY_COLUMNS-1):
            #                         enemy_position_y = enemy_positions_list[last_enemy_row][last_enemy_column].y
            #                 else:
            #                     enemy_positions_list[i][j].y += 3
            #                     if (i == ENEMY_ROWS-1) and (j == ENEMY_COLUMNS-1):
            #                         enemy_direction = False
            #                         enemy_position_y -= 2
            #         else:
            #             if enemy_positions_list[last_enemy_row][last_enemy_column].x > 40:
            #                 enemy_positions_list[i][j].x -= 3
            #             else:
            #                 if enemy_position_y != enemy_positions_list[last_enemy_row][last_enemy_column].y:
            #                     enemy_positions_list[i][j].x -= 3
            #                     if (i == ENEMY_ROWS - 1) and (j == ENEMY_COLUMNS - 1):
            #                         enemy_position_y = enemy_positions_list[last_enemy_row][last_enemy_column].y
            #                 else:
            #                     enemy_positions_list[i][j].y += 3
            #                     if (i == ENEMY_ROWS - 1) and (j == ENEMY_COLUMNS - 1):
            #                         enemy_direction = True
            #                         enemy_position_y -= 2

                # Animate enemies
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

    SCREEN.fill((0, 0, 0))
    SCREEN.blit(player, (player_position.x, player_position.y))
    for i in range(ENEMY_ROWS):
        for j in range(ENEMY_COLUMNS):
            # Check if enemy hit bullet
            if bullet_shot == True and enemy_death_list[i][j] == False:
                if (enemy_positions_list[i][j].x + 3 < bullet_position.x <
                        enemy_positions_list[i][j].x + ENEMY_WIDTH - 3) and \
                        bullet_position.y < enemy_positions_list[i][j].y + ENEMY_HEIGHT:
                    enemy_death_list[i][j] = True
                    bullet_shot = False

            # Display enemy if alive
            if enemy_timer_list[i][j] > 0:
                SCREEN.blit(enemy_list[i][j], (enemy_positions_list[i][j].x, enemy_positions_list[i][j].y))
    SCREEN.blit(bullet, (bullet_position.x, bullet_position.y))

    for i in range(28, 230):
        # Do not draw line at positions in linebreak_list to display destroyed areas
        if i in linebreak_list:
            continue
        # Draw line one pixel at a time
        SCREEN.set_at((i, 15), (255, 255, 255))
    pygame.display.flip()

pygame.quit()
