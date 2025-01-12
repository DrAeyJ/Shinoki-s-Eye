import os
import random
import sqlite3
import sys
import time
import pygame
import datetime


class Starting_screen:
    def __init__(self):
        global active_scr
        active_scr = self

        self.options_opened = False

        bkgr = pygame.sprite.Sprite(start_scr_sprites_group)
        bkgr.image = load_image("Sprites/logo.png")
        bkgr.rect = bkgr.image.get_rect()
        bkgr.rect.x = -10
        bkgr.rect.y = 0

        play = pygame.sprite.Sprite(start_scr_sprites_group)
        play.image = load_image("Sprites/play_btn_spr.png")
        play.rect = bkgr.image.get_rect()
        play.rect.x = 203
        play.rect.y = 253

        options = pygame.sprite.Sprite(start_scr_sprites_group)
        options.image = load_image("Sprites/options_btn_spr.png")
        options.rect = bkgr.image.get_rect()
        options.rect.x = 203
        options.rect.y = 333

        quits = pygame.sprite.Sprite(start_scr_sprites_group)
        quits.image = load_image("Sprites/quit_btn_spr.png")
        quits.rect = bkgr.image.get_rect()
        quits.rect.x = 203
        quits.rect.y = 413

    def render(self, scrn):
        if not self.options_opened:
            start_scr_sprites_group.draw(screen)

            start_btn = button(scrn, (0, 79, 153), 200, 250, 300, 50, 3)
            options_btn = button(scrn, (0, 79, 153), 200, 330, 300, 50, 3)
            quit_btn = button(scrn, (0, 79, 153), 200, 410, 300, 50, 3)

            start_btn.assign_func(PreGameRoom)
            options_btn.assign_func(self.options)
            quit_btn.assign_func(sys.exit)
        else:
            pass

    def options(self):
        self.options_opened = True


class Game:
    def __init__(self):
        global active_scr
        active_scr = self

        global game
        game = self

        self.spr_frame = 0
        self.clock = pygame.time.Clock()
        self.spr_time = 0

        self.stage = 1
        self.room = 1

        self.spr_time = 0
        self.clock = pygame.time.Clock()

        self.options_opened = False

        self.player_x = 0
        self.player_y = 0

        self.left = 275
        self.top = 50

        self.board = [[0] * 12 for _ in range(12)]
        self.escape_hatch = None

        self.con = sqlite3.connect("data/Shinoki`s Eye.sqlite")
        self.cur = self.con.cursor()

        self.gameplay()

    def generate_room(self, stage):
        self.board = [[0] * 12 for _ in range(12)]
        for k in range(len(self.board[0])):
            for j in range(len(self.board[0])):
                if k == 0 and j == 0:
                    pass
                else:
                    chance = random.randint(0, 100)
                    if 0 <= chance < 15:
                        self.board[k][j] = ["wall", 3 * stage]
                    elif 15 <= chance < 25:
                        enemy = str(random.choice(self.cur.execute(f"""select name 
                        from enemies 
                        where stage = {stage}""").fetchall()))[2:-3]
                        self.board[k][j] = ["enemy", enemy]
                    elif 25 <= chance < 30:
                        self.board[k][j] = ["chest",]
        self.generate_escape_hatch()

    def interact(self, cell_x, cell_y, keys):
        if self.board[cell_x][cell_y] == 0:
            self.move(25, keys)

        elif self.board[cell_x][cell_y][0] == "wall":
            pass

        elif self.board[cell_x][cell_y][0] == "enemy":
            pass
#       future func enemy_movement()

        elif self.board[cell_x][cell_y][0] == "chest":
            pass
#           future func open_chest()

    def move(self, iterations, direction):
        for _ in range(iterations):
            time.sleep(0.01 / iterations)

            if direction == "w":
                self.player_y -= 1 / iterations
            elif direction == "a":
                self.player_x -= 1 / iterations
            elif direction == "s":
                self.player_y += 1 / iterations
            elif direction == "d":
                self.player_x += 1 / iterations

            screen.fill((0, 0, 0))
            active_scr.render(screen)
            pygame.display.flip()
        self.player_x = round(self.player_x)
        self.player_y = round(self.player_y)
        if self.board[self.player_x][self.player_y] == "escape_hatch":
            ShopRoom()

    def render(self, scr):
        scr.fill((0, 0, 0))
        global board_img
        global player_spr
        global entities
        global wall_img

        board_img.image = load_image(f"Sprites/Board{self.stage}.png")
        board_img.rect = board_img.image.get_rect()
        board_img.rect.x = 500 - 200 * self.player_x
        board_img.rect.y = 250 - 200 * self.player_y
        board_group.draw(scr)

        player_spr.image = load_image(f"Sprites/King{self.spr_frame}.png")
        player_spr.rect = player_spr.image.get_rect()
        player_spr.rect.x = 500
        player_spr.rect.y = 250
        player.draw(scr)

        for i in range(len(self.board[0])):
            for j in range(len(self.board[0])):
                if self.board[i][j] != 0 and self.board[i][j][0] == "wall":
                    wall_img.image = load_image("Sprites/Wall1.png")
                    wall_img.rect = wall_img.image.get_rect()
                    wall_img.rect.x = 500 + 200 * i - 200 * self.player_x
                    wall_img.rect.y = 250 + 200 * j - 200 * self.player_y
                    wall_gr.draw(scr)

        self.spr_time += self.clock.tick() / 1000
        if self.spr_time >= 0.5 and not self.spr_frame:
            self.spr_frame = 1
            self.spr_time = 0
        elif self.spr_time >= 0.5 and self.spr_frame:
            self.spr_frame = 0
            self.spr_time = 0

    def gameplay(self):
        self.generate_room(1)

    def generate_escape_hatch(self):
        self.escape_hatch = [random.randint(0, 11), random.randint(0, 11)]
        if self.escape_hatch[0] <= 3 and self.escape_hatch[1] <= 3:
            self.generate_escape_hatch()
        else:
            self.board[self.escape_hatch[0]][self.escape_hatch[1]] = "escape_hatch"


class ShopRoom:
    pass


class PreGameRoom(Game):
    def __init__(self):
        super().__init__()
        self.clock = pygame.time.Clock()
        global starting_time
        starting_time = datetime.datetime.now()

    def render(self, scr):
        scr.fill((0, 0, 0))

        global board_img
        global player_spr

        board_img.image = load_image("Sprites/Board0.png")
        board_img.rect = board_img.image.get_rect()
        board_img.rect.x = 500 - 200 * self.player_x
        board_img.rect.y = 250 - 200 * self.player_y
        board_group.draw(scr)

        player_spr.image = load_image(f"Sprites/King{self.spr_frame}.png")
        player_spr.rect = player_spr.image.get_rect()
        player_spr.rect.x = 500
        player_spr.rect.y = 250
        player.draw(scr)

        self.spr_time += self.clock.tick() / 1000
        if self.spr_time >= 0.5 and not self.spr_frame:
            self.spr_frame = 1
            self.spr_time = 0
        elif self.spr_time >= 0.5 and self.spr_frame:
            self.spr_frame = 0
            self.spr_time = 0

        self.gameplay()

    def gameplay(self):
        if (5 <= self.player_x <= 6
                and 5 <= self.player_y <= 6):
            screen.fill((0, 0, 0))
            Game()


class button:
    def __init__(self, scrn, clr, x, y, x1, y1, w):
        self.scrn = scrn
        self.clr = clr
        self.x = x
        self.y = y
        self.xlen = x1
        self.ylen = y1
        self.w = w
        pygame.draw.rect(scrn, clr, ((x, y), (x1, y1)), w,
                         3, 3)
        self.mouse_drawn()

    def mouse_drawn(self):
        if event.type == pygame.MOUSEMOTION:
            if self.x < event.pos[0] < self.x + self.xlen and self.y < event.pos[1] < self.y + self.ylen:
                pygame.draw.rect(self.scrn, pygame.Color('yellow'),
                                 ((self.x, self.y), (self.xlen, self.ylen)), self.w,
                                 3, 3)

    def assign_func(self, f, *args):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.x < event.pos[0] < self.x + self.xlen and self.y < event.pos[1] < self.y + self.ylen:
                f(*args)


def load_image(nm, colorkey=None):
    name = os.path.join("data", nm)
    if not os.path.isfile(name):
        print(f"Lacking file '{name}' in game folder.")
        sys.exit()
    image = pygame.image.load(name)
    return image


pygame.init()
size = 1200, 700
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Shinoki`s Eye")

start_scr_sprites_group = pygame.sprite.Group()
board_group = pygame.sprite.Group()
player = pygame.sprite.Group()
entity_gr = pygame.sprite.Group()
wall_gr = pygame.sprite.Group()
board_img = pygame.sprite.Sprite(board_group)
wall_img = pygame.sprite.Sprite(wall_gr)
player_spr = pygame.sprite.Sprite(player)
entities = pygame.sprite.Sprite(entity_gr)

start_scr = Starting_screen()
active_scr = start_scr

starting_time = None
ending_time = None
game_duration = None

pregamewait = False
game = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE] and active_scr == Starting_screen and active_scr.options_opened:
            active_scr.options_opened = False
        if key[pygame.K_ESCAPE] and game:
            game.options_opened = True
        if key[pygame.K_ESCAPE] and game and game.options_opened:
            game.options_opened = True
        if key[pygame.K_ESCAPE] and not game:
            sys.exit()

        if game:
            if event.type == pygame.KEYDOWN:
                if key[pygame.K_w]:
                    if game.player_y in range(0, 11):
                        game.interact(game.player_x, game.player_y - 1, "w")
                elif key[pygame.K_a]:
                    if game.player_x - 1 in range(0, 11):
                        game.interact(game.player_x - 1, game.player_y, "a")
                elif key[pygame.K_s]:
                    if game.player_y + 1 in range(0, 11):
                        game.interact(game.player_x, game.player_y - 1, "s")
                elif key[pygame.K_d]:
                    if game.player_x + 1 in range(0, 11):
                        game.interact(game.player_x + 1, game.player_y, "d")
    screen.fill((0, 0, 0))
    active_scr.render(screen)
    pygame.display.flip()
pygame.quit()
