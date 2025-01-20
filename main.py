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
        bkgr.rect.x = 0
        bkgr.rect.y = 0

        play = pygame.sprite.Sprite(start_scr_sprites_group)
        play.image = load_image("Sprites/play_btn_spr.png")
        play.rect = bkgr.image.get_rect()
        play.rect.x = 403
        play.rect.y = 333

        options = pygame.sprite.Sprite(start_scr_sprites_group)
        options.image = load_image("Sprites/options_btn_spr.png")
        options.rect = bkgr.image.get_rect()
        options.rect.x = 403
        options.rect.y = 418

        quits = pygame.sprite.Sprite(start_scr_sprites_group)
        quits.image = load_image("Sprites/quit_btn_spr.png")
        quits.rect = bkgr.image.get_rect()
        quits.rect.x = 403
        quits.rect.y = 503

    def render(self, scrn):
        if not self.options_opened:
            start_scr_sprites_group.draw(screen)

            start_btn = button(scrn, (0, 79, 153), 400, 330, 400, 50, 3)
            options_btn = button(scrn, (0, 79, 153), 400, 415, 400, 50, 3)
            quit_btn = button(scrn, (0, 79, 153), 400, 500, 400, 50, 3)

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

        global ultra_game
        ultra_game = self

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

        self.board = [[0] * 8 for _ in range(8)]
        self.escape_hatch = None

        self.maxhp = 12
        self.hp = 12
        self.equipped_weapon = ""
        self.dmg = 3

        self.item_sold = False

        self.con = sqlite3.connect("data/Shinoki`s Eye.sqlite")
        self.cur = self.con.cursor()

        self.gameplay()

    def generate_room(self, stage):
        self.board = [[0] * 8 for _ in range(8)]
        for k in range(len(self.board[0])):
            for j in range(len(self.board[0])):
                if k == 0 and j == 0:
                    pass
                else:
                    chance = random.randint(0, 100)
                    if 0 <= chance < 15:
                        self.board[k][j] = ["wall", 3 * stage]
                    elif 15 <= chance < 25:
                        if k > 1 and j > 1:
                            enemy = str(random.choice(self.cur.execute(f"""select name 
                            from enemies 
                            where stage = {stage}""").fetchall()))[2:-3]
                            self.board[k][j] = ["enemy", enemy]
                    elif 25 <= chance < 30:
                        self.board[k][j] = ["chest",]
        self.generate_escape_hatch()

    def interact(self, cell_x, cell_y, keys):
        if (self.board[cell_x][cell_y] == 0 or
                self.board[cell_x][cell_y] == "escape_hatch"):
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
            time.sleep(0.4 / iterations)

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
        global esha_img
        global loading

        if loading:
            if 0 <= self.spr_time / 1000 <= 3:
                player_spr.image = load_image(f"Sprites/Kinglying.png")
                player_spr.rect = player_spr.image.get_rect()
                player_spr.rect.x = 500
                player_spr.rect.y = 250
                player.draw(scr)
            elif 3 < self.spr_time / 1000 <= 5:
                player_spr.image = load_image(f"Sprites/King0.png")
                player_spr.rect = player_spr.image.get_rect()
                player_spr.rect.x = 500
                player_spr.rect.y = 250
                player.draw(scr)
            else:
                loading = False
            self.spr_time += self.clock.tick()

        else:
            board_img.image = load_image(f"Sprites/Board{self.stage}8x8.png")
            board_img.rect = board_img.image.get_rect()
            board_img.rect.x = 500 - 200 * self.player_x
            board_img.rect.y = 250 - 200 * self.player_y

            board_group.draw(scr)

            esha_img.image = load_image(f"Sprites/escape_hatch{self.spr_frame}.png")
            esha_img.rect = esha_img.image.get_rect()
            esha_img.rect.x = 500 + 200 * self.escape_hatch[0] - 200 * self.player_x
            esha_img.rect.y = 250 + 200 * self.escape_hatch[1] - 200 * self.player_y

            esha_gr.draw(scr)

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
                    if self.board[i][j] != 0 and self.board[i][j][0] == "enemy" and (self.board[i][j][1] == "Skeleton" or
                                                                                     self.board[i][j][1] == "Looker"):
                        entities.image = load_image(f"Sprites/{self.board[i][j][1]}{self.spr_frame}.png")
                        entities.rect = entities.image.get_rect()
                        entities.rect.x = 500 + 200 * i - 200 * self.player_x
                        entities.rect.y = 250 + 200 * j - 200 * self.player_y
                        entity_gr.draw(scr)

            self.spr_time += self.clock.tick() / 1000
            if self.spr_time >= 0.5 and not self.spr_frame:
                self.spr_frame = 1
                self.spr_time = 0
            elif self.spr_time >= 0.5 and self.spr_frame:
                self.spr_frame = 0
                self.spr_time = 0

            health_img.image = load_image(f"Sprites/HealthBar1.png")
            health_img.rect = health_img.image.get_rect()
            health_img.rect.x = 450
            health_img.rect.y = 600

            health_gr.draw(scr)

    def gameplay(self):
        self.generate_room(1)
        for klh in self.board:
            print(klh)

    def generate_escape_hatch(self):
        self.escape_hatch = [random.randint(0, 7), random.randint(0, 7)]
        if self.escape_hatch[0] <= 3 and self.escape_hatch[1] <= 3:
            self.generate_escape_hatch()
        else:
            self.board[self.escape_hatch[0]][self.escape_hatch[1]] = "escape_hatch"

    def switch_room(self):
        global game
        global active_scr
        global loading

        loading = True

        self.room += 1
        self.player_x, self.player_y = 0, 0
        self.generate_room(1)
        self.spr_time = 0
        self.clock.tick()

        game = self
        active_scr = self


class ShopRoom:
    def __init__(self):
        self.player_x = 2
        self.player_y = 3
        self.spr_time = 0
        self.spr_frame = 0
        self.clock = pygame.time.Clock()
        self.board = [[0] * 5 for _ in range(5)]
        self.escape_hatch = [2, 0]

        self.board[1][1] = ["trader", "Kuro"]
        self.board[2][1] = ["trader", "Shroom"]
        self.board[3][1] = ["trader", "Shiro"]

        global active_scr
        active_scr = self

        global game
        game = self

        self.item1 = []
        self.item2 = []
        self.choice = False

        self.con = sqlite3.connect("data/Shinoki`s Eye.sqlite")
        self.cur = self.con.cursor()

        self.item_sold = False

    def render(self, scr):
        global board_img
        global player_spr
        global entities
        global esha_img
        global item_img

        if [self.player_x, self.player_y] == self.escape_hatch:
            global ultra_game

            ultra_game.switch_room()

        if self.choice:
            item1 = button(scr, (0, 79, 153), 100, 150, 400, 400, 3)
            item2 = button(scr, (0, 79, 153), 700, 150, 400, 400, 3)
            item1.assign_func(take_item, *self.item1)
            item2.assign_func(take_item, *self.item2)

            item_img.image = load_image(f"Sprites/{self.item1[0]}.png")
            item_img.rect = item_img.image.get_rect()
            item_img.rect.x = 100
            item_img.rect.y = 150

            item_gr.draw(scr)

            item_img.image = load_image(f"Sprites/{self.item2[0]}.png")
            item_img.rect = item_img.image.get_rect()
            item_img.rect.x = 700
            item_img.rect.y = 150

            item_gr.draw(scr)
        else:
            board_img.image = load_image(f"Sprites/ShopRoom.png")
            board_img.rect = board_img.image.get_rect()
            board_img.rect.x = 500 - 200 * self.player_x
            board_img.rect.y = 250 - 200 * self.player_y

            board_group.draw(scr)

            if self.item_sold:
                esha_img.image = load_image(f"Sprites/escape_hatch{self.spr_frame}.png")
                esha_img.rect = esha_img.image.get_rect()
                esha_img.rect.x = 500 + 200 * self.escape_hatch[0] - 200 * self.player_x
                esha_img.rect.y = 250 + 200 * self.escape_hatch[1] - 200 * self.player_y
            else:
                esha_img.image = load_image(f"Sprites/escape_hatch0.png")
                esha_img.rect = esha_img.image.get_rect()
                esha_img.rect.x = 500 + 200 * self.escape_hatch[0] - 200 * self.player_x
                esha_img.rect.y = 250 + 200 * self.escape_hatch[1] - 200 * self.player_y

            esha_gr.draw(scr)

            player_spr.image = load_image(f"Sprites/King{self.spr_frame}.png")
            player_spr.rect = player_spr.image.get_rect()
            player_spr.rect.x = 500
            player_spr.rect.y = 250

            player.draw(scr)

            for i in range(len(self.board[0])):
                for j in range(len(self.board[0])):
                    if self.board[i][j] != 0 and self.board[i][j][0] == "trader":
                        entities.image = load_image(f"Sprites/{self.board[i][j][1]}{self.spr_frame}.png")
                        entities.rect = entities.image.get_rect()
                        entities.rect.x = 500 + 200 * i - 200 * self.player_x
                        entities.rect.y = 250 + 200 * j - 200 * self.player_y
                        entity_gr.draw(scr)

            self.spr_time += self.clock.tick() / 1000
            if self.spr_time >= 0.5 and not self.spr_frame:
                self.spr_frame = 1
                self.spr_time = 0
            elif self.spr_time >= 0.5 and self.spr_frame:
                self.spr_frame = 0
                self.spr_time = 0

            health_img.image = load_image(f"Sprites/HealthBar1.png")
            health_img.rect = health_img.image.get_rect()
            health_img.rect.x = 450
            health_img.rect.y = 600

            health_gr.draw(scr)

    def interact(self, cell_x, cell_y, keys):
        if (self.board[cell_x][cell_y] == 0 or
                self.board[cell_x][cell_y] == "escape_hatch"):
            self.move(25, keys)
        elif self.board[cell_x][cell_y][0] == "trader" and not self.item_sold:
            chance = random.randint(0, 100)
            if 0 < chance < 30:
                self.item1 = str(random.choice(self.cur.execute(f"""select name, type, healsordamages 
                from items 
                where dropstage = 1
                and type like 'Damages'
                and weapontype like '{self.board[cell_x][cell_y][1]}'""").fetchall()))[2:-2].split("', '")
            else:
                self.item1 = str(random.choice(self.cur.execute(f"""select name, type, healsordamages 
                from items 
                where dropstage = 1
                and type like 'Heals'""").fetchall()))[2:-2].split("', '")
            chance = random.randint(0, 100)
            if 0 < chance < 30:
                self.item2 = str(random.choice(self.cur.execute(f"""select name, type, healsordamages 
                            from items 
                            where dropstage = 1
                            and type like 'Damages'
                            and weapontype like '{self.board[cell_x][cell_y][1]}'""").fetchall()))[2:-2].split("', '")
            else:
                self.item2 = str(random.choice(self.cur.execute(f"""select name, type, healsordamages 
                            from items 
                            where dropstage = 1
                            and type like 'Heals'""").fetchall()))[2:-2].split("', '")
            self.choice = True

    def move(self, iterations, direction):
        for _ in range(iterations):
            time.sleep(0.4 / iterations)

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
        super().__init__()
        self.clock = pygame.time.Clock()
        global starting_time
        starting_time = datetime.datetime.now()

    def render(self, scr):
        scr.fill((0, 0, 0))
        global board_img
        global player_spr
        global loading

        if loading:
            if 0 <= self.spr_time / 1000 <= 3:
                player_spr.image = load_image(f"Sprites/Kinglying.png")
                player_spr.rect = player_spr.image.get_rect()
                player_spr.rect.x = 500
                player_spr.rect.y = 250
                player.draw(scr)
            elif 3 < self.spr_time / 1000 <= 4:
                player_spr.image = load_image(f"Sprites/King0.png")
                player_spr.rect = player_spr.image.get_rect()
                player_spr.rect.x = 500
                player_spr.rect.y = 250
                player.draw(scr)
            elif 4 < self.spr_time / 1000 <= 4.5:
                player_spr.image = load_image(f"Sprites/Kingblink.png")
                player_spr.rect = player_spr.image.get_rect()
                player_spr.rect.x = 500
                player_spr.rect.y = 250
                player.draw(scr)
            elif 4.5 < self.spr_time / 1000 <= 6:
                player_spr.image = load_image(f"Sprites/King0.png")
                player_spr.rect = player_spr.image.get_rect()
                player_spr.rect.x = 500
                player_spr.rect.y = 250
                player.draw(scr)
            else:
                loading = False
            self.spr_time += self.clock.tick()

        else:
            board_img.image = load_image("Sprites/Board08x8.png")
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
        if (3 <= self.player_x <= 4
                and 3 <= self.player_y <= 4):
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


def take_item(name, typ, amount):
    global ultra_game
    global game
    if typ == "Damages":
        if "-" in amount:
            am = [int(i) for i in amount.split(" - ")]
            ultra_game.maxhp = 12 - am[1]
            ultra_game.dmg = am[0]
            ultra_game.equipped_weapon = name
        elif "+" in amount:
            am = [int(i) for i in amount.split(" + ")]
            ultra_game.maxhp = 12 + am[1]
            ultra_game.dmg = am[0]
            ultra_game.equipped_weapon = name
        else:
            ultra_game.dmg = amount
            ultra_game.equipped_weapon = name
    elif typ == "Heals":
        ultra_game.hp += int(amount)
        if ultra_game.hp > ultra_game.maxhp:
            ultra_game.hp = ultra_game.maxhp

    game.item_sold = True
    game.choice = False


pygame.init()
size = 1200, 700
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Shinoki`s Eye")

start_scr_sprites_group = pygame.sprite.Group()
board_group = pygame.sprite.Group()
player = pygame.sprite.Group()
entity_gr = pygame.sprite.Group()
wall_gr = pygame.sprite.Group()
esha_gr = pygame.sprite.Group()
item_gr = pygame.sprite.Group()
health_gr = pygame.sprite.Group()

board_img = pygame.sprite.Sprite(board_group)
esha_img = pygame.sprite.Sprite(esha_gr)
wall_img = pygame.sprite.Sprite(wall_gr)
player_spr = pygame.sprite.Sprite(player)
entities = pygame.sprite.Sprite(entity_gr)
item_img = pygame.sprite.Sprite(item_gr)
health_img = pygame.sprite.Sprite(health_gr)

start_scr = Starting_screen()
active_scr = start_scr

starting_time = None
ending_time = None
game_duration = None

pregamewait = False
game = None
ultra_game = None

loading = True

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        key = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:
            if key[pygame.K_ESCAPE] and active_scr == Starting_screen and active_scr.options_opened:
                active_scr.options_opened = False
            if key[pygame.K_ESCAPE] and game and not game.options_opened:
                game.options_opened = True
            elif key[pygame.K_ESCAPE] and game and game.options_opened:
                game.options_opened = False

            if game:
                if key[pygame.K_w]:
                    if game.player_y - 1 in range(0, 11):
                        game.interact(game.player_x, game.player_y - 1, "w")
                elif key[pygame.K_a]:
                    if game.player_x - 1 in range(0, 11):
                        game.interact(game.player_x - 1, game.player_y, "a")
                elif key[pygame.K_s]:
                    if game.player_y + 1 in range(0, 11):
                        game.interact(game.player_x, game.player_y + 1, "s")
                elif key[pygame.K_d]:
                    if game.player_x + 1 in range(0, 11):
                        game.interact(game.player_x + 1, game.player_y, "d")
    screen.fill((0, 0, 0))
    active_scr.render(screen)
    pygame.display.flip()
pygame.quit()
