import os
import sys
import time
import pygame


class Starting_screen:
    def __init__(self):
        global active_scr
        active_scr = self

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
        start_scr_sprites_group.draw(screen)

        start_btn = button(scrn, (0, 79, 153), 200, 250, 300, 50, 3)
        options_btn = button(scrn, (0, 79, 153), 200, 330, 300, 50, 3)
        quit_btn = button(scrn, (0, 79, 153), 200, 410, 300, 50, 3)

        start_btn.assign_func(PreGameRoom)
        options_btn.assign_func(Options)
        quit_btn.assign_func(sys.exit)


class Options:
    def __init__(self):
        global start_scr_active
        start_scr_active = False

        global active_scr
        active_scr = self


class Game:
    def __init__(self):
        global start_scr_active
        start_scr_active = False

        global active_scr
        active_scr = self

        global game
        game = self

        self.player_x = 0
        self.player_y = 0

        self.board = [[0] * 12 for _ in range(12)]
        self.left = 275
        self.top = 50


class PreGameRoom(Game):
    def __init__(self):
        super().__init__()
        self.board = pygame.sprite.Sprite(board_group)

    def render(self, scr):
        scr.fill((0, 0, 0))

        self.board.image = load_image("Sprites/Board1_borderless.png")
        self.board.rect = self.board.image.get_rect()
        self.board.rect.x = - 100 + 600 - 200 * self.player_x
        self.board.rect.y = - 100 + 350 - 200 * self.player_y

        self.enter_game()
        board_group.draw(scr)

    def enter_game(self):
        if (self.player_x == 11
                and self.player_y in [5, 6]):
            Game()


class Ingame_Settings:
    def __init__(self):
        global active_scr
        active_scr = self


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

start_scr = Starting_screen()
active_scr = start_scr
start_scr_active = True

active_entities = []

pregamewait = False
game = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE] and not start_scr_active:
            Ingame_Settings()
        if key[pygame.K_ESCAPE] and start_scr_active:
            sys.exit()

        if game:
            if event.type == pygame.KEYDOWN:
                if key[pygame.K_w]:
                    for i in range(50):
                        time.sleep(0.004)
                        game.player_y -= 0.02
                        screen.fill((0, 0, 0))
                        active_scr.render(screen)
                        pygame.display.flip()
                elif key[pygame.K_a]:
                    for i in range(50):
                        time.sleep(0.004)
                        game.player_x -= 0.02
                        screen.fill((0, 0, 0))
                        active_scr.render(screen)
                        pygame.display.flip()
                elif key[pygame.K_d]:
                    for i in range(50):
                        time.sleep(0.004)
                        game.player_x += 0.02
                        screen.fill((0, 0, 0))
                        active_scr.render(screen)
                        pygame.display.flip()
                elif key[pygame.K_s]:
                    for i in range(50):
                        time.sleep(0.004)
                        game.player_y += 0.02
                        screen.fill((0, 0, 0))
                        active_scr.render(screen)
                        pygame.display.flip()
    screen.fill((0, 0, 0))
    active_scr.render(screen)
    pygame.display.flip()
pygame.quit()
