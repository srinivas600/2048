import pygame
import random
import math

pygame.init()

FPS, WIDTH, HIGHT = 60, 800, 800

ROWS, COLS = 4, 4

RECT_HEIGHT, RECT_WIDTH = 200, 200

OUTLINE_COLOR = (187, 173, 160)
OUTLINE_THICKNESS = 10
BAGROUND_COLOR = (198, 192, 190)
FONT_COLOR = (119, 110, 101)

FONT = pygame.font.SysFont("comicsans", 60, bold= True)
MOVE_LEV = 20

WINDOW = pygame.display.set_mode((WIDTH, HIGHT))
pygame.display.set_caption("2048")

class Tiles:
    COLORS = [(237, 229, 218), 
             (238, 225, 201),
             (243, 178, 122), 
             (246, 150, 101), 
             (247, 124, 95), 
             (247, 95, 59),
             (237, 208, 115),
             (237, 204, 99),
             (236, 202, 80)]
    
    def __init__(self, value, row, col) -> None:
        self.value = value
        self.row = row
        self.col = col
        self.x = col * RECT_WIDTH
        self.y = row * RECT_HEIGHT
    
    def get_color(self):
        color_idx = int(math.log2(self.value)) - 1
        color = self.COLORS[color_idx]
        return color
        
    def draw(self, window):
        color = self.get_color()
        pygame.draw.rect(window, color, (self.x, self.y, RECT_HEIGHT, RECT_HEIGHT))
        
        text = FONT.render(str(self.value), 1, FONT_COLOR)
        window.blit(
            text,
            (
                self.x + (RECT_WIDTH / 2  - text.get_width() / 2),
                self.y + (RECT_HEIGHT / 2 - text.get_height() / 2)
            )
        )
        
   
    
    def set_pos(self, ceil = False):
        if ceil:
            self.row = math.ceil(self.y / RECT_HEIGHT)
            self.col = math.ceil(self.x / RECT_WIDTH)
        else:
            self.row = math.floor(self.y / RECT_HEIGHT)
            self.col = math.floor(self.x / RECT_WIDTH)
    
    def move(self, delta):
        self.x += delta[0]
        self.y += delta[1]
        return


def draw_grid(window):
    for r in range(1, 4):
        y = r * RECT_HEIGHT
        pygame.draw.line(window, OUTLINE_COLOR, (0, y), (WIDTH, y), OUTLINE_THICKNESS)
    
    for c in range(1, 4):
        x = c * RECT_WIDTH
        pygame.draw.line(window, OUTLINE_COLOR, (x, 0), (x, WIDTH), OUTLINE_THICKNESS)
            
    pygame.draw.rect(window, OUTLINE_COLOR, (0, 0, WIDTH, HIGHT), OUTLINE_THICKNESS)

def draw(window, tiles):
    window.fill(BAGROUND_COLOR)
    
    for tile in tiles.values():
        tile.draw(window)
        
    draw_grid(window)
    pygame.display.update()

def get_random_pos(tiles):
    row = None
    col = None
    while True:
        row = random.randrange(0, ROWS)
        col = random.randrange(0, COLS)
        
        if f"{row}{col}" not in tiles:
            break
        
    return row, col

def move_tiles(window, tiles, clock, direction):
    updated = True
    blocks = set()
    
    if direction == "L":
        sort_fun = lambda x : x.col
        reverse = False
        delta = (-MOVE_LEV, 0)
        boundary_check = lambda tile: tile.col == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col - 1}")
        merge_check = lambda tile, next_tile: tile.x > next_tile.x + MOVE_LEV
        move_check = (lambda tile, next_tile: tile.x > next_tile.x + MOVE_LEV + RECT_WIDTH)
        ceil = True
        
    elif direction == "R":
        sort_fun = lambda x : x.col
        reverse = True
        delta = (MOVE_LEV, 0)
        boundary_check = lambda tile: tile.col == COLS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col + 1}")
        merge_check = lambda tile, next_tile: tile.x < next_tile.x - MOVE_LEV
        move_check = (lambda tile, next_tile: tile.x + RECT_WIDTH + MOVE_LEV < next_tile.x)
        ceil = False
    
    elif direction == "U":
        sort_fun = lambda x : x.row
        reverse = False
        delta = (0, -MOVE_LEV)
        boundary_check = lambda tile: tile.row == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row - 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y > next_tile.y + MOVE_LEV
        move_check = (lambda tile, next_tile: tile.y > next_tile.y + MOVE_LEV + RECT_HEIGHT)
        ceil = True
    
    elif direction == "D":
        sort_fun = lambda x : x.row
        reverse = True
        delta = (0, MOVE_LEV)
        boundary_check = lambda tile: tile.row == ROWS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row + 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y < next_tile.y - MOVE_LEV
        move_check = (lambda tile, next_tile: tile.y + RECT_HEIGHT + MOVE_LEV < next_tile.y)
        ceil = False
    
    while updated:
        clock.tick(FPS)
        updated = False
        sorted_tiles = sorted(tiles.values(), key = sort_fun, reverse = reverse)
        
        for i, ele in enumerate(sorted_tiles):
            if boundary_check(ele):
                continue
            
            next_tile = get_next_tile(ele)
            if not next_tile:
                ele.move(delta)
            elif ele.value == next_tile.value and ele not in blocks and next_tile not in blocks:
                if merge_check(ele, next_tile):
                    ele.move(delta)
                else:
                    next_tile.value *= 2
                    sorted_tiles.pop(i)
                    blocks.add(next_tile)
            
            elif move_check(ele, next_tile):
                ele.move(delta)
            else:
                continue
            
            ele.set_pos(ceil)
            updated = True
        update_tiles(window, tiles, sorted_tiles)
    
    return end_move(tiles)
    
def end_move(tiles):
    if len(tiles) == 16:
        return False
    
    row, col = get_random_pos(tiles)
    tiles[f"{row}{col}"] = Tiles(random.choice([2, 4]), row, col)
    return True
    
def update_tiles(window, tiles, sorted_tiles):
    tiles.clear()
    for tile in sorted_tiles:
        tiles[f"{tile.row}{tile.col}"] = tile
    
    draw(window, tiles)
        
def generate_tiles():
    tiles = {}
    for _ in range(2):
        row, col = get_random_pos(tiles)
        tiles[f"{row}{col}"] = Tiles(2, row, col)
    
    return tiles


def main(window):
    clock = pygame.time.Clock()
    run = True
    
    tiles = generate_tiles()
    
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                run = False
                break
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_tiles(window, tiles, clock, "L")
                if event.key == pygame.K_RIGHT:
                    move_tiles(window, tiles, clock, "R")
                if event.key == pygame.K_UP:
                    move_tiles(window, tiles, clock, "U")
                if event.key == pygame.K_DOWN:
                    move_tiles(window, tiles, clock, "D")    
            
            
        draw(window, tiles)
    pygame.quit()


if __name__ == "__main__":
    main(WINDOW)
