import pygame


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
    return create_clock().tick(fps)

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

def check_key_press(key):
    return get_all_keys_state()[key]

def move_object_and_account_delta_time(object, speed: int, dt):
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





initialize_pygame_modules()
SCREEN = initialize_display_window()

player = create_surface(16, 8)

spritesheet = load_image('sheet.png')
draw_surface_on_surface(spritesheet, player, (0, 0), (1, 49, 16, 8))
player_position = assign_coordinates(128, 200)

enemy_direction = True  #True = right; False = left
previous_second = 0 #No function
current_second = 0  #No function

ENEMY_ROWS, ENEMY_COLUMNS = set_enemy_list_dimensions(5, 11)
enemy_positions_list = initialize_2d_list(player_position, ENEMY_ROWS, ENEMY_COLUMNS)
enemy_death_list = initialize_2d_list(False, ENEMY_ROWS, ENEMY_COLUMNS)
enemy_timer_list = initialize_2d_list(1.00, ENEMY_ROWS, ENEMY_COLUMNS)


# player_position assigned by default to set correct data type of Vector2 to values

# Stores which enemies are dead

# Dead enemies play death animation until timer runs out

# Helps assign positions to enemies by updating values in these variables during below loop
assign_coordinates_to_positions_list(enemy_positions_list, ENEMY_ROWS, ENEMY_COLUMNS, 40, 60)


ENEMY_WIDTH = 16
ENEMY_HEIGHT = 8
enemy_list = initialize_2d_list(player, ENEMY_ROWS, ENEMY_COLUMNS)
for i in range(ENEMY_ROWS):
    for j in range(ENEMY_COLUMNS):
        enemy = create_surface(16, 8)
        enemy_list[i][j] = enemy

bullet = create_surface(1, 4)
draw_surface_on_surface(spritesheet, bullet, (0, 0), (55, 53, 1, 4))
gun_position = assign_coordinates(136, 200)
bullet_position = gun_position  # 'Stores' bullet in gun of spaceship by default

# Row and column of the last enemy in the list when traversed column-by-column instead of the normal row-by-row looping
# left-to-right list traversal for right travel direction, and right-to-left traversal for left direction
# (default is for bottom-rightmost enemy)
last_enemy_row = ENEMY_ROWS - 1
last_enemy_column = ENEMY_COLUMNS - 1

linebreak_list = [] # Line is broken at which locations
bullet_shot = False
game_running = True
create_clock()

enemy_position_y = 0
while game_running:
    delta_time = set_delta_time(144)
    current_second = int(pygame.time.get_ticks() / 1000)    # No function

    for event in get_events_from_queue():
        game_running = check_quit_event(event)

    if check_key_press(pygame.K_SPACE) and bullet_shot == False:
        bullet_position = assign_coordinates(gun_position.x, gun_position.y)
        bullet_shot = True
        play_sound_from_channel('shoot.wav', 1)
    if check_key_press(pygame.K_LEFT) and player_position.x > 30:
        player_position.x -= 100 * delta_time
        gun_position.x -= 100 * delta_time
    elif check_key_press(pygame.K_RIGHT) and player_position.x < 220:
        player_position.x += 100 * delta_time
        gun_position.x += 100 * delta_time

    # Bullet destroys line where it hits
    if bullet_position.y < 15:
        bullet_shot = False
        add_item_in_front_of_list(linebreak_list, int(bullet_position.x))

    if bullet_shot:
        bullet_position.y -= 200 * delta_time
    else:
        bullet_position = gun_position  #  Bullet respawns at gun_position

    # Updates coordinates of the last enemy when an enemy is killed, based on the direction of travel
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
                    draw_surface_on_surface(spritesheet, enemy_list[i][j], (0, 0), (55, 1, 16, 8))
                else:
                    enemy_timer_list[i][j] = 0  # Death animation finished, enemy removed
            else:

                # Animate enemies
                if i == 0:
                    if current_second % 2 == 0:
                        draw_surface_on_surface(spritesheet, enemy_list[i][j], (0, 0), (1, 1, 16, 8))
                    elif current_second % 2 == 1:
                        draw_surface_on_surface(spritesheet, enemy_list[i][j], (0, 0), (1, 11, 16, 8))
                elif i == 1 or i == 2:
                    if current_second % 2 == 0:
                        draw_surface_on_surface(spritesheet, enemy_list[i][j], (0, 0), (19, 1, 16, 8))
                    elif current_second % 2 == 1:
                        draw_surface_on_surface(spritesheet, enemy_list[i][j], (0, 0), (19, 11, 16, 8))
                else:
                    if current_second % 2 == 0:
                        draw_surface_on_surface(spritesheet, enemy_list[i][j], (0, 0), (37, 1, 16, 8))
                    elif current_second % 2 == 1:
                        draw_surface_on_surface(spritesheet, enemy_list[i][j], (0, 0), (37, 11, 16, 8))
    previous_second = current_second

    fill_surface_with_color(SCREEN, (0, 0, 0))
    draw_surface_on_surface(player, SCREEN, (player_position.x, player_position.y), (0, 0, 16, 8))
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
                draw_surface_on_surface(enemy_list[i][j], SCREEN, (enemy_positions_list[i][j].x, enemy_positions_list[i][j].y), (0, 0, 16, 8))
    draw_surface_on_surface(bullet, SCREEN, (bullet_position.x, bullet_position.y), (0, 0, 1, 4))

    for i in range(28, 230):
        # Do not draw line at positions in linebreak_list to display destroyed areas
        if i in linebreak_list:
            continue
        # Draw line one pixel at a time
        draw_coloured_pixel_on_surface(SCREEN, (i, 15), (255, 255, 255))
    update_display_surface()

quit_game()