import os
import random
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

        self.spr_time = 0
        self.clock = pygame.time.Clock()

        self.options_opened = False

        self.player_x = 0
        self.player_y = 0

        self.left = 275
        self.top = 50

        self.board = [[0] * 12 for _ in range(12)]

        self.gameplay()

    def gameplay(self):
        pass

    def generate_room(self, stage):
        self.board = [[0] * 12 for _ in range(12)]
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if i != 0 and j != 0:
                    chance = random.randint(0, 100)
                    if 0 <= chance < 35:
                        self.board[i][j] = ("wall", 3 * stage)
                    elif 35 <= chance < 50:
                        self.board[i][j] = ("enemy", 25 * stage)
                    elif 50 <= chance < 55:
                        self.board[i][j] = ("chest", None)

    def interact(self, cell_x, cell_y, keys):
        if self.board[cell_x][cell_y] == 0:
            match keys:
                case "w":
                    self.move(25, "w")
                case "a":
                    self.move(25, "a")
                case "s":
                    self.move(25, "s")
                case "d":
                    self.move(25, "d")

        elif self.board[cell_x][cell_y][0] == "wall":
            if self.board[cell_x][cell_y][1] == 1:
                self.board[cell_x][cell_y] = 0
            else:
                self.board[cell_x][cell_y][1] -= 1

        elif self.board[cell_x][cell_y][0] == "enemy":
            pass
#           future func enemy_movement()

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


class PreGameRoom(Game):
    def __init__(self):
        self.spr_frame = False
        super().__init__()
        self.board_img = pygame.sprite.Sprite(board_group)
        self.player_spr = pygame.sprite.Sprite(board_group1)
        self.player_spr1 = pygame.sprite.Sprite(board_group2)

        self.clock = pygame.time.Clock()
        self.spr_time = 0
        global starting_time
        starting_time = datetime.datetime.now()

    def render(self, scr):
        scr.fill((0, 0, 0))

        self.board_img.image = load_image("Sprites/Board0.png")
        self.board_img.rect = self.board_img.image.get_rect()
        self.board_img.rect.x = 500 - 200 * self.player_x
        self.board_img.rect.y = 250 - 200 * self.player_y

        board_group.draw(scr)

        if not self.spr_frame:
            self.player_spr.image = load_image("Sprites/King.png")
            self.player_spr.rect = self.player_spr.image.get_rect()
            self.player_spr.rect.x = 500
            self.player_spr.rect.y = 250
            board_group1.draw(scr)
        elif self.spr_frame:
            self.player_spr1.image = load_image("Sprites/King1.png")
            self.player_spr1.rect = self.player_spr1.image.get_rect()
            self.player_spr1.rect.x = 500
            self.player_spr1.rect.y = 250
            board_group2.draw(scr)

        self.spr_time += self.clock.tick() / 1000
        if self.spr_time >= 0.5 and not self.spr_frame:
            self.spr_frame = True
            self.spr_time = 0
        elif self.spr_time >= 0.5 and self.spr_frame:
            self.spr_frame = False
            self.spr_time = 0

        self.gameplay()

    def gameplay(self):
        if (5 <= self.player_x <= 6
                and 5 <= self.player_y <= 6):
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
board_group1 = pygame.sprite.Group()
board_group2 = pygame.sprite.Group()

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
                    game.interact(game.player_x, game.player_y - 1, "w")
                elif key[pygame.K_a]:
                    game.interact(game.player_x - 1, game.player_y, "a")
                elif key[pygame.K_s]:
                    game.interact(game.player_x + 1, game.player_y, "s")
                elif key[pygame.K_d]:
                    game.interact(game.player_x, game.player_y + 1, "d")
    screen.fill((0, 0, 0))
    active_scr.render(screen)
    pygame.display.flip()
pygame.quit()
