import pygame
import os
import pickle
from button import Button


pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
LOWER_MARGIN = 100
SIDE_MARGIN = 300

screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption('Level Editor')

clock = pygame.time.Clock()
FPS = 60
#define game variables 
ROWS = 16
MAX_COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPES = 21
level = 0
current_tile = 0
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 1


# load tiles
tiles = []
num_of_imgs = len(os.listdir("./assets/tiles"))

i = 0
for i in range(num_of_imgs):
    img = pygame.image.load(f"./assets/tiles/{i}.png").convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    tiles.append(img)


# load background images
pine1_img = pygame.image.load('./assets/background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('./assets/background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('./assets/background/mountain.png').convert_alpha()
sky_img = pygame.image.load('./assets/background/sky_cloud.png').convert_alpha()

background_img_list = [pine1_img, pine2_img, mountain_img, sky_img]

save_img = pygame.image.load("./assets/save_btn.png").convert_alpha()
load_img = pygame.image.load("./assets/load_btn.png").convert_alpha()
# define colors
GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (200, 25, 25)

# define font
font = pygame.font.SysFont('Futura', 30)

# create world data list
world_data = []
for i in range(ROWS):
    r = [-1] * MAX_COLS
    world_data.append(r)

# create ground
for tile in range(MAX_COLS):
    world_data[ROWS - 1][tile] = 0


# function for outputting text to screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# create function for drawing background
def draw_bg():
    screen.fill(GREEN)

    width = sky_img.get_width()

    for i in range(4):
        offset = width * i
        screen.blit(sky_img , (-scroll * .5 + offset, 0))
        screen.blit(mountain_img, (-scroll * .6 + offset, SCREEN_HEIGHT - mountain_img.get_height() - 150))
        screen.blit(pine1_img, (-scroll * .7 + offset, SCREEN_HEIGHT - pine1_img.get_height() - 50))
        screen.blit(pine2_img, (-scroll * .8 + offset, SCREEN_HEIGHT - pine2_img.get_height() + 120))

# draw grid
def draw_grid():
    """Draws the grid over the background"""

    # vertical lines
    for i in range(MAX_COLS + 1):
        pygame.draw.line(screen, WHITE, (i * TILE_SIZE - scroll, 0), (i * TILE_SIZE - scroll, SCREEN_HEIGHT))

    # horizontal lines
    for i in range(MAX_COLS + 1):
        pygame.draw.line(screen, WHITE, (0, i * TILE_SIZE), (SCREEN_WIDTH, TILE_SIZE * i))
    

def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(tiles[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))



# create buttons
save_button = Button(SCREEN_WIDTH //2, SCREEN_HEIGHT + LOWER_MARGIN - 50, save_img, 1)
load_button = Button(SCREEN_WIDTH //2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 50, load_img, 1)
# makes empty button list
button_list = []
button_col = 0
button_row = 0

for tile in tiles:
    tile_button = Button(SCREEN_WIDTH + (75 * button_col) + 50, (75 * button_row) + 50, tile, 1)
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:
        button_col = 0
        button_row += 1
    



"""Main game loop"""
running = True
while running:

    clock.tick(FPS)
    draw_bg()
    draw_grid()
    draw_world()

    draw_text(f'Level: {level}', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)
    draw_text('Press UP or DOWN to change level', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 50)

    # save and load data
    if save_button.draw(screen):
        pickle_out = open(f'level{level}_data', 'wb')
        pickle.dump(world_data, pickle_out)
        pickle_out.close()

    if load_button.draw(screen):
        scroll = 0
        world_data = []
        pickle_in = open(f'./level_data/level{level}_data', 'rb')
        world_data = pickle.load(pickle_in)

    # draw tile panel and tiles
    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, .8, SIDE_MARGIN, SCREEN_HEIGHT + 1))

    # choose a tile
    button_count = 0
    for button_count, button in enumerate(button_list):
        if button.draw(screen):
            current_tile = button_count
    
    pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)


    # scroll the map
    if scroll_left and scroll > 0:
        scroll -= 5 * scroll_speed
    if scroll_right and scroll < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
        scroll += 5 * scroll_speed


    # add new tiles to screen
    # get mouse position
    pos = pygame.mouse.get_pos()
    x = (pos[0] + scroll) // TILE_SIZE
    y = pos[1] // TILE_SIZE

    # check that the mouse coordinates are within the Scren
    if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
        # update tile values
        if pygame.mouse.get_pressed()[0] == 1:
             if world_data[y][x] != current_tile:
                 world_data[y][x] = current_tile
        elif pygame.mouse.get_pressed()[2] == 1:
            if world_data[y][x] != -1:
                world_data[y][x] = -1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_UP:
                level += 1
            if event.key == pygame.K_DOWN:
                if level > 0:
                    level -= 1
            if event.key == pygame.K_RIGHT:
                scroll_right = True
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                scroll_speed = 5
            if event.key == pygame.K_ESCAPE:
                running = False

        # keyboard release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                scroll_speed = 1

    pygame.display.update()

pygame.quit()