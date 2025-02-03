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

        reset_stats()

    def render(self, scrn):
        start_scr_sprites_group.draw(screen)

        start_btn = button(scrn, (0, 79, 153), 400, 330, 400, 50, 3)
        options_btn = button(scrn, (0, 79, 153), 400, 415, 400, 50, 3)
        quit_btn = button(scrn, (0, 79, 153), 400, 500, 400, 50, 3)

        start_btn.assign_func(PreGameRoom)
        options_btn.assign_func(Options)
        quit_btn.assign_func(sys.exit)


class Options:
    def __init__(self):
        global active_scr
        active_scr = self

        self.stats_showing = False

        file = open("data/stats.txt", "r")
        self.content = [int(i) for i in file.read().split("\n")]
        file.close()

    def render(self, scr):
        global keys_used
        global choice_btn_img

        if not self.stats_showing:
            control_btn = button(scr, (0, 79, 153), 400, 50, 400, 100, 3)
            stats_btn = button(scr, (0, 79, 153), 400, 200, 400, 100, 3)
            back_btn = button(scr, (0, 79, 153), 950, 550, 200, 100, 3)

            control_btn.assign_func(self.change_controls)
            stats_btn.assign_func(self.show_stats)
            back_btn.assign_func(Starting_screen)

            choice_btn_img.image = load_image(f"Sprites/control_btn_img_{keys_used}.png")
            choice_btn_img.rect = choice_btn_img.image.get_rect()
            choice_btn_img.rect.x = 403
            choice_btn_img.rect.y = 53
            choice_btn_gr.draw(scr)

            choice_btn_img.image = load_image(f"Sprites/stats_btn_img.png")
            choice_btn_img.rect = choice_btn_img.image.get_rect()
            choice_btn_img.rect.x = 403
            choice_btn_img.rect.y = 203
            choice_btn_gr.draw(scr)

            choice_btn_img.image = load_image(f"Sprites/back_btn_img.png")
            choice_btn_img.rect = choice_btn_img.image.get_rect()
            choice_btn_img.rect.x = 953
            choice_btn_img.rect.y = 553
            choice_btn_gr.draw(scr)

        elif self.stats_showing:
            strin = game_over_font.render(f"STATS", 1, (0, 79, 153))
            str_rect = strin.get_rect()
            str_rect.y = 25
            str_rect.x = 425
            screen.blit(strin, str_rect)

            strin = healordmg_font.render(f"Games played: {self.content[0]}", 1, pygame.Color('white'))
            strin_rect = strin.get_rect()
            strin_rect.y = 150
            strin_rect.x = 450
            screen.blit(strin, strin_rect)

            strin = healordmg_font.render(f"Games won: {self.content[1]}", 1, pygame.Color('white'))
            strin_rect = strin.get_rect()
            strin_rect.y = 200
            strin_rect.x = 470
            screen.blit(strin, strin_rect)

            strin = healordmg_font.render(f"Games lost: {self.content[2]}", 1, pygame.Color('white'))
            strin_rect = strin.get_rect()
            strin_rect.y = 250
            strin_rect.x = 475
            screen.blit(strin, strin_rect)

            strin = healordmg_font.render(f"Total kills: {self.content[3]}", 1, pygame.Color('white'))
            strin_rect = strin.get_rect()
            strin_rect.y = 325
            strin_rect.x = 490
            screen.blit(strin, strin_rect)

            strin = healordmg_font.render(f"Chests opened: {self.content[4]}", 1, pygame.Color('white'))
            strin_rect = strin.get_rect()
            strin_rect.y = 375
            strin_rect.x = 450
            screen.blit(strin, strin_rect)

            strin = healordmg_font.render(f"Total damage: {self.content[5]}", 1, pygame.Color('white'))
            strin_rect = strin.get_rect()
            strin_rect.y = 450
            strin_rect.x = 460
            screen.blit(strin, strin_rect)

            strin = healordmg_font.render(f"Total HP healed: {self.content[6]}", 1, pygame.Color('white'))
            strin_rect = strin.get_rect()
            strin_rect.y = 500
            strin_rect.x = 440
            screen.blit(strin, strin_rect)

            strin = healordmg_font.render(f"Steps made: {self.content[7]}", 1, pygame.Color('white'))
            strin_rect = strin.get_rect()
            strin_rect.y = 550
            strin_rect.x = 470
            screen.blit(strin, strin_rect)

            strin = healordmg_font.render(f"Total score: {self.content[8]}", 1, pygame.Color('white'))
            strin_rect = strin.get_rect()
            strin_rect.y = 625
            strin_rect.x = 470
            screen.blit(strin, strin_rect)

            back_btn = button(scr, (0, 79, 153), 950, 50, 200, 100, 3)
            back_btn.assign_func(Options)
            choice_btn_img.image = load_image(f"Sprites/back_btn_img.png")
            choice_btn_img.rect = choice_btn_img.image.get_rect()
            choice_btn_img.rect.x = 953
            choice_btn_img.rect.y = 53
            choice_btn_gr.draw(scr)

    def change_controls(self):
        global keys_used

        if keys_used == "WASD":
            keys_used = "Arrows"
        elif keys_used == "Arrows":
            keys_used = "WASD"

        time.sleep(0.5)

    def show_stats(self):
        self.stats_showing = True

    def dont_show_stats(self):
        self.stats_showing = False


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

        self.choice = False
        self.item = []
        self.xp_amount = 0
        self.xp_time = 0
        self.heal_time = 0
        self.amount = 0
        self.dmg_x = 0
        self.dmg_y = 0

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
                            enemy = list(random.choice(self.cur.execute(f"""select name, hp, atk, type 
                            from enemies 
                            where stage = {stage}
                            and type like 'Hostile'""").fetchall()))
                            self.board[k][j] = ["enemy", enemy[0], enemy[1], int(enemy[2]), enemy[3]]
                    elif 25 <= chance < 28:
                        self.board[k][j] = ["chest",]
        enemy = list(random.choice(self.cur.execute(f"""select name, hp, atk, type 
        from enemies 
        where stage = {stage}
        and type like 'Neutral'""").fetchall()))
        self.board[random.randint(1, 7)][random.randint(1, 7)] = ["enemy", enemy[0], enemy[1], int(enemy[2]), enemy[3]]
        self.generate_escape_hatch()

    def interact(self, cell_x, cell_y, keys):
        if (self.board[cell_x][cell_y] == 0 or
                self.board[cell_x][cell_y] == "escape_hatch"):
            self.move(25, keys)
        elif self.board[cell_x][cell_y][0] == "wall":
            pass

        elif self.board[cell_x][cell_y][0] == "chest":
            self.open_chest()
            self.board[cell_x][cell_y] = 0

        elif self.board[cell_x][cell_y][0] == "enemy":
            if self.board[cell_x][cell_y][4] == "Neutral":
                self.open_chest(trader=True)
                self.board[cell_x][cell_y] = 0

    def move(self, iterations, direction):
        global loading
        global steps_made

        if not loading:
            if not self.choice:
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
                self.attack()

                steps_made += 1

    def render(self, scr):
        scr.fill((0, 0, 0))
        global board_img
        global player_spr
        global entities
        global wall_img
        global chest_img
        global esha_img
        global loading
        global hpfont
        global room_img
        global choice_btn_img

        if loading:
            if 0 <= self.spr_time / 1000 <= 1.5:
                player_spr.image = load_image(f"Sprites/Kinglying.png")
                player_spr.rect = player_spr.image.get_rect()
                player_spr.rect.x = 500
                player_spr.rect.y = 250
                player.draw(scr)
            elif 1.5 < self.spr_time / 1000 <= 3:
                player_spr.image = load_image(f"Sprites/King0.png")
                player_spr.rect = player_spr.image.get_rect()
                player_spr.rect.x = 500
                player_spr.rect.y = 250
                player.draw(scr)
            else:
                loading = False
            self.spr_time += self.clock.tick()

        elif self.choice:
            item = button(scr, (0, 79, 153), 400, 50, 400, 400, 3)
            take = button(scr, (0, 79, 153), 650, 525, 400, 100, 3)
            loose = button(scr, (0, 79, 153), 150, 525, 400, 100, 3)

            choice_btn_img.image = load_image(f"Sprites/lose_btn_img.png")
            choice_btn_img.rect = choice_btn_img.image.get_rect()
            choice_btn_img.rect.x = 153
            choice_btn_img.rect.y = 528

            choice_btn_gr.draw(scr)

            choice_btn_img.image = load_image(f"Sprites/take_btn_img.png")
            choice_btn_img.rect = choice_btn_img.image.get_rect()
            choice_btn_img.rect.x = 653
            choice_btn_img.rect.y = 528

            choice_btn_gr.draw(scr)

            take.assign_func(take_item, *self.item)
            loose.assign_func(loose_item)

            item_img.image = load_image(f"Sprites/{self.item[0]}.png")
            item_img.rect = item_img.image.get_rect()
            item_img.rect.x = 400
            item_img.rect.y = 50

            item_gr.draw(scr)

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
                    if self.board[i][j] != 0 and self.board[i][j][0] == "chest":
                        chest_img.image = load_image("Sprites/Chest.png")
                        chest_img.rect = chest_img.image.get_rect()
                        chest_img.rect.x = 500 + 200 * i - 200 * self.player_x
                        chest_img.rect.y = 250 + 200 * j - 200 * self.player_y
                        chest_gr.draw(scr)
                    if self.board[i][j] != 0 and self.board[i][j][0] == "enemy":
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

            if 0.2 <= self.hp < self.maxhp * 0.4:
                health_img.image = load_image(f"Sprites/Health4.png")
                health_img.rect = health_img.image.get_rect()
                health_img.rect.x = 450
                health_img.rect.y = 600
            elif 0.4 <= self.hp < self.maxhp * 0.6:
                health_img.image = load_image(f"Sprites/Health3.png")
                health_img.rect = health_img.image.get_rect()
                health_img.rect.x = 450
                health_img.rect.y = 600
            elif 0.6 <= self.hp < self.maxhp * 0.8:
                health_img.image = load_image(f"Sprites/Health2.png")
                health_img.rect = health_img.image.get_rect()
                health_img.rect.x = 450
                health_img.rect.y = 600
            elif 0.8 <= self.hp <= self.maxhp:
                health_img.image = load_image(f"Sprites/Health1.png")
                health_img.rect = health_img.image.get_rect()
                health_img.rect.x = 450
                health_img.rect.y = 600
            else:
                health_img.image = load_image(f"Sprites/Health5.png")
                health_img.rect = health_img.image.get_rect()
                health_img.rect.x = 450
                health_img.rect.y = 600

            health_gr.draw(scr)
            strin = hpfont.render(f"{self.hp}/{self.maxhp}", 1, pygame.Color('white'))
            hp_rect = strin.get_rect()
            hp_rect.y = 570
            hp_rect.x = 575
            screen.blit(strin, hp_rect)

            if self.heal_time <= 15:
                if self.amount != 0:
                    if self.amount > 0:
                        heal = healordmg_font.render(f"+{self.amount}", 1, pygame.Color('green'))
                        heal_rect = heal.get_rect()
                        heal_rect.y = 325
                        heal_rect.x = 590
                        screen.blit(heal, heal_rect)
                    else:
                        dmg = healordmg_font.render(f"{self.amount}", 1, pygame.Color('red'))
                        dmg_rect = dmg.get_rect()
                        dmg_rect.y = 325
                        dmg_rect.x = 590
                        screen.blit(dmg, dmg_rect)
                        dmg = healordmg_font.render(f"-{self.dmg}", 1, pygame.Color('red'))
                        dmg_rect = dmg.get_rect()
                        dmg_rect.y = 325 + (self.dmg_y - self.player_y) * 200
                        dmg_rect.x = 590 + (self.dmg_x - self.player_x) * 200
                        screen.blit(dmg, dmg_rect)
                self.heal_time += self.clock.tick()

            if self.xp_time <= 15:
                if self.xp_amount != 0:
                    if self.xp_amount > 0:
                        xp = healordmg_font.render(f"+{self.xp_amount}XP", 1, pygame.Color('yellow'))
                        xp_rect = xp.get_rect()
                        xp_rect.y = 345
                        xp_rect.x = 20
                        screen.blit(xp, xp_rect)
                self.xp_time += self.clock.tick()

            room_img.image = load_image(f"Sprites/Room{str(self.room)}.png")
            room_img.rect = room_img.image.get_rect()
            room_img.rect.x = 550
            room_img.rect.y = 50

            room_gr.draw(scr)

    def gameplay(self):
        self.generate_room(1)

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
        global score

        for _ in range(8):
            print("\n")

        if self.room < 7:
            loading = True

            self.room += 1
            self.player_x, self.player_y = 0, 0
            self.generate_room(1)
            self.spr_time = 0
            self.clock.tick()

            game = self
            active_scr = self

            adding = random.randint(400, 600)
            score += adding
            self.xp_amount = adding
            self.xp_time = 0
        else:
            You_win()

    def open_chest(self, trader=False):
        global score
        global chests_opened

        if not trader:
            self.item = chance = random.randint(0, 100)
            if 0 < chance < 10:
                self.item = str(random.choice(self.cur.execute(f"""select name, type, healsordamages 
                from items 
                where dropstage = 1
                and type like 'Damages'""").fetchall()))[2:-2].split("', '")
            else:
                self.item = str(random.choice(self.cur.execute(f"""select name, type, healsordamages 
                from items 
                where dropstage = 1
                and type like 'Heals'""").fetchall()))[2:-2].split("', '")
            self.choice = True
            chests_opened += 1
        elif trader:
            self.item = str(random.choice(self.cur.execute(f"""select name, type, healsordamages 
                from items 
                where dropstage = 1
                and type like 'Damages'""").fetchall()))[2:-2].split("', '")
            self.choice = True

    def attack(self):
        global score
        global enemies_killed
        global damage_dealt

        for i in range(self.player_x - 1, self.player_x + 2):
            for j in range(self.player_y - 1, self.player_y + 2):
                try:
                    if i in range(0, 8):
                        if j in range(0, 8):
                            if self.board[i][j] != 0:
                                if self.board[i][j][0] == "enemy":
                                    if self.board[i][j][4] == "Hostile":
                                        self.board[i][j][2] -= int(self.dmg)
                                        damage_dealt += int(self.dmg)
                                        self.amount = -self.board[i][j][3]
                                        self.heal_time = 0
                                        self.hp -= self.board[i][j][3]
                                        if self.hp <= 0:
                                            Game_over(self.room)
                                        self.dmg_x = i
                                        self.dmg_y = j
                                        if self.board[i][j][2] <= 0:
                                            self.board[i][j] = 0
                                            adding = random.randint(75, 100)
                                            score += adding
                                            self.xp_amount = adding
                                            self.xp_time = 0
                                            enemies_killed += 1
                except IndexError:
                    pass


class ShopRoom:
    def __init__(self):
        self.player_x = 2
        self.player_y = 3
        self.hp, self.maxhp = ultra_game.hp, ultra_game.maxhp
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
        self.heal_time = 0
        self.amount = 0

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

            if 0.2 <= self.hp < self.maxhp * 0.4:
                health_img.image = load_image(f"Sprites/Health4.png")
                health_img.rect = health_img.image.get_rect()
                health_img.rect.x = 450
                health_img.rect.y = 600
            elif 0.4 <= self.hp < self.maxhp * 0.6:
                health_img.image = load_image(f"Sprites/Health3.png")
                health_img.rect = health_img.image.get_rect()
                health_img.rect.x = 450
                health_img.rect.y = 600
            elif 0.6 <= self.hp < self.maxhp * 0.8:
                health_img.image = load_image(f"Sprites/Health2.png")
                health_img.rect = health_img.image.get_rect()
                health_img.rect.x = 450
                health_img.rect.y = 600
            elif 0.8 <= self.hp <= self.maxhp:
                health_img.image = load_image(f"Sprites/Health1.png")
                health_img.rect = health_img.image.get_rect()
                health_img.rect.x = 450
                health_img.rect.y = 600
            else:
                health_img.image = load_image(f"Sprites/Health5.png")
                health_img.rect = health_img.image.get_rect()
                health_img.rect.x = 450
                health_img.rect.y = 600

            health_gr.draw(scr)
            strin = hpfont.render(f"{self.hp}/{self.maxhp}", 1, pygame.Color('white'))
            hp_rect = strin.get_rect()
            hp_rect.y = 570
            hp_rect.x = 575
            screen.blit(strin, hp_rect)

            if self.heal_time <= 20:
                if self.amount != 0:
                    if self.amount > 0:
                        heal = healordmg_font.render(f"+{self.amount}", 1, pygame.Color('green'))
                        heal_rect = heal.get_rect()
                        heal_rect.y = 325
                        heal_rect.x = 590
                        screen.blit(heal, heal_rect)
                self.heal_time += self.clock.tick()

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

    def attack(self):
        pass

    def move(self, iterations, direction):
        global steps_made

        if not self.choice:
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

        steps_made += 1


class PreGameRoom(Game):
    def __init__(self):
        super().__init__()
        self.clock = pygame.time.Clock()

        global starting_time
        starting_time = datetime.datetime.now()

        global loading
        loading = True

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

    def attack(self):
        pass


class Game_over:
    def __init__(self, stage):
        self.stage = stage - 1

        global active_scr
        active_scr = self

        global ultra_game
        ultra_game = None

        global game
        game = None

        self.clock = pygame.time.Clock()
        self.time = 0

        global starting_time
        global ending_time
        global game_duration
        ending_time = datetime.datetime.now()
        game_duration = ending_time - starting_time

        write_file("Lost")

    def render(self, scr):
        global player_spr
        global gameover_btn_img
        global score
        global game_duration

        player_spr.image = load_image(f"Sprites/Kinglying.png")
        player_spr.rect = player_spr.image.get_rect()
        player_spr.rect.x = 500
        player_spr.rect.y = 250
        player.draw(scr)

        if self.time / 1000 >= 4:
            strin = game_over_font.render(f"GAME OVER", 1, pygame.Color('red'))
            str_rect = strin.get_rect()
            str_rect.y = 50
            str_rect.x = 275
            screen.blit(strin, str_rect)
            strin = healordmg_font.render(f"Your Score is {score}", 1, pygame.Color('white'))
            str_rect = strin.get_rect()
            str_rect.y = 175
            str_rect.x = 450
            screen.blit(strin, str_rect)
            strin = healordmg_font.render(f"Your Time in Game is {str(game_duration)[:7]}",
                                          1, pygame.Color('white'))
            str_rect = strin.get_rect()
            str_rect.y = 225
            str_rect.x = 350
            screen.blit(strin, str_rect)
            strin = healordmg_font.render(f"Rooms passed: {self.stage}",
                                          1, pygame.Color('white'))
            str_rect = strin.get_rect()
            str_rect.y = 275
            str_rect.x = 450
            screen.blit(strin, str_rect)

        if self.time / 1000 >= 7:
            mainmenu_btn = button(scr, (0, 79, 153), 650, 525, 400, 100, 3)
            quit_btn = button(scr, (0, 79, 153), 150, 525, 400, 100, 3)

            mainmenu_btn.assign_func(Starting_screen)
            quit_btn.assign_func(sys.exit)

            gameover_btn_img.image = load_image("Sprites/quit_btn_spr1.png")
            gameover_btn_img.rect = gameover_btn_img.image.get_rect()
            gameover_btn_img.rect.x = 153
            gameover_btn_img.rect.y = 528

            gameover_gr.draw(scr)

            gameover_btn_img.image = load_image("Sprites/main_menu_btn_spr.png")
            gameover_btn_img.rect = gameover_btn_img.image.get_rect()
            gameover_btn_img.rect.x = 653
            gameover_btn_img.rect.y = 528

            gameover_gr.draw(scr)

        self.time += self.clock.tick()


class You_win:
    def __init__(self):
        global active_scr
        active_scr = self

        global ultra_game
        ultra_game = None

        global game
        game = None

        self.clock = pygame.time.Clock()
        self.time = 0
        self.spr_clock = pygame.time.Clock()
        self.spr_time = 0
        self.spr_frame = "0"
        self.moving = False

        global starting_time
        global ending_time
        global game_duration
        ending_time = datetime.datetime.now()
        game_duration = ending_time - starting_time

        write_file("Won")

    def render(self, scr):
        global player_spr
        global gameover_btn_img
        global score
        global game_duration
        global chests_opened
        global enemies_killed

        if not self.moving:
            player_spr.image = load_image(f"Sprites/King{self.spr_frame}.png")
            player_spr.rect = player_spr.image.get_rect()
            player_spr.rect.x = 500
            player_spr.rect.y = 250
            player.draw(scr)
        if self.moving:
            player_spr.image = load_image(f"Sprites/King{self.spr_frame}.png")
            player_spr.rect = player_spr.image.get_rect()
            player_spr.rect.x = 500 + 200 * (self.time / 1000 - 2)
            player_spr.rect.y = 250
            player.draw(scr)

        if self.time / 1000 >= 2:
            self.moving = True

        if self.time / 1000 >= 9:
            player_spr.image = load_image(f"Sprites/Shinoki`sEye.png")
            player_spr.rect = player_spr.image.get_rect()
            player_spr.rect.x = 550
            player_spr.rect.y = 0
            player.draw(scr)

        if self.time / 1000 >= 6:
            strin = game_over_font.render(f"YOU WIN", 1, pygame.Color('yellow'))
            str_rect = strin.get_rect()
            str_rect.y = 75
            str_rect.x = 50
            screen.blit(strin, str_rect)

        if self.time / 1000 >= 10:
            strin = healordmg_font.render(f"Your Score is {score}", 1, pygame.Color('white'))
            str_rect = strin.get_rect()
            str_rect.y = 250
            str_rect.x = 50
            screen.blit(strin, str_rect)

        if self.time / 1000 >= 11:
            strin = healordmg_font.render(f"Your Time in Game is {str(game_duration)[:7]}",
                                          1, pygame.Color('white'))
            str_rect = strin.get_rect()
            str_rect.y = 300
            str_rect.x = 50
            screen.blit(strin, str_rect)

        if self.time / 1000 >= 12:
            strin = healordmg_font.render(f"Enemies killed: {enemies_killed}",
                                          1, pygame.Color('white'))
            str_rect = strin.get_rect()
            str_rect.y = 350
            str_rect.x = 50
            screen.blit(strin, str_rect)

        if self.time / 1000 >= 13:
            strin = healordmg_font.render(f"Chests opened: {chests_opened}",
                                          1, pygame.Color('white'))
            str_rect = strin.get_rect()
            str_rect.y = 400
            str_rect.x = 50
            screen.blit(strin, str_rect)

        if self.time / 1000 >= 14:
            mainmenu_btn = button(scr, (0, 79, 153), 650, 525, 400, 100, 3)
            quit_btn = button(scr, (0, 79, 153), 150, 525, 400, 100, 3)

            mainmenu_btn.assign_func(Starting_screen)
            quit_btn.assign_func(sys.exit)

            you_win_img.image = load_image("Sprites/quit_btn_spr1.png")
            you_win_img.rect = you_win_img.image.get_rect()
            you_win_img.rect.x = 153
            you_win_img.rect.y = 528

            you_win_gr.draw(scr)

            you_win_img.image = load_image("Sprites/main_menu_btn_spr.png")
            you_win_img.rect = you_win_img.image.get_rect()
            you_win_img.rect.x = 653
            you_win_img.rect.y = 528

            you_win_gr.draw(scr)

        if not self.moving:
            if self.spr_time >= 1 and self.spr_frame == "0":
                self.spr_frame = "blink"
                self.spr_time = 0
            elif self.spr_time >= 0.4 and self.spr_frame == "blink":
                self.spr_frame = "0"
                self.spr_time = 0
        else:
            if self.spr_time >= 0.5 and self.spr_frame == "0":
                self.spr_frame = "1"
                self.spr_time = 0
            elif self.spr_time >= 0.5 and self.spr_frame == "1":
                self.spr_frame = "0"
                self.spr_time = 0

        self.spr_time += self.spr_clock.tick() / 1000
        self.time += self.clock.tick()


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
    global score
    global hp_healed

    game.spr_time = 0
    if typ == "Damages":
        if "-" in amount:
            am = [int(i) for i in amount.split(" - ")]
            ultra_game.maxhp = 12 - am[1]
            ultra_game.dmg = am[0]
            ultra_game.equipped_weapon = name
            if ultra_game != game:
                game.maxhp = 12 - am[1]
        elif "+" in amount:
            am = [int(i) for i in amount.split(" + ")]
            ultra_game.maxhp = 12 + am[1]
            ultra_game.dmg = am[0]
            ultra_game.equipped_weapon = name
            if ultra_game != game:
                game.maxhp = 12 + am[1]
        else:
            ultra_game.dmg = amount
            ultra_game.equipped_weapon = name
        if ultra_game.hp > ultra_game.maxhp:
            ultra_game.hp = ultra_game.maxhp
            game.hp = ultra_game.maxhp
    elif typ == "Heals":
        hp_healed += int(amount)

        if ultra_game is game:
            ultra_game.hp += int(amount)
            ultra_game.amount = int(amount)
            ultra_game.heal_time = 0
        if ultra_game != game:
            game.hp += int(amount)
            game.amount = int(amount)
            game.heal_time = 0
            ultra_game.hp += int(amount)
            ultra_game.amount = int(amount)
    if game.hp > game.maxhp:
        ultra_game.hp = ultra_game.maxhp
        game.hp = ultra_game.maxhp

    if game is ultra_game:
        adding = random.randint(25, 50)
        score += adding
        ultra_game.xp_amount = adding
        ultra_game.xp_time = 0

    game.item_sold = True
    game.choice = False


def loose_item():
    game.choice = False


def write_file(result):
    global score
    global enemies_killed
    global chests_opened
    global damage_dealt
    global hp_healed
    global steps_made

    file = open("data/stats.txt", "r")
    content = [int(i) for i in file.read().split("\n")]
    file.close()

    content[0] += 1
    if result == "Won":
        content[1] += 1
    elif result == "Lost":
        content[2] += 1
    content[3] += enemies_killed
    content[4] += chests_opened
    content[5] += damage_dealt
    content[6] += hp_healed
    content[7] += steps_made
    content[8] += score

    for i in range(len(content)):
        content[i] = str(content[i])
    file = open("data/stats.txt", "w")
    file.write("\n".join(content))
    file.close()


def reset_stats():
    global game_duration
    global score
    global enemies_killed
    global chests_opened
    global damage_dealt
    global hp_healed
    global steps_made

    game_duration, score, enemies_killed, chests_opened, damage_dealt, hp_healed, steps_made = 0, 0, 0, 0, 0, 0, 0


pygame.init()
size = 1200, 700
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Shinoki`s Eye")

start_scr_sprites_group = pygame.sprite.Group()
board_group = pygame.sprite.Group()
player = pygame.sprite.Group()
entity_gr = pygame.sprite.Group()
wall_gr = pygame.sprite.Group()
chest_gr = pygame.sprite.Group()
esha_gr = pygame.sprite.Group()
room_gr = pygame.sprite.Group()
item_gr = pygame.sprite.Group()
choice_btn_gr = pygame.sprite.Group()
health_gr = pygame.sprite.Group()
gameover_gr = pygame.sprite.Group()
you_win_gr = pygame.sprite.Group()
controls_btn_gr = pygame.sprite.Group()

board_img = pygame.sprite.Sprite(board_group)
esha_img = pygame.sprite.Sprite(esha_gr)
wall_img = pygame.sprite.Sprite(wall_gr)
chest_img = pygame.sprite.Sprite(chest_gr)
player_spr = pygame.sprite.Sprite(player)
entities = pygame.sprite.Sprite(entity_gr)
room_img = pygame.sprite.Sprite(room_gr)
item_img = pygame.sprite.Sprite(item_gr)
choice_btn_img = pygame.sprite.Sprite(choice_btn_gr)
health_img = pygame.sprite.Sprite(health_gr)
gameover_btn_img = pygame.sprite.Sprite(gameover_gr)
you_win_img = pygame.sprite.Sprite(you_win_gr)
controls_btn_img = pygame.sprite.Sprite(controls_btn_gr)

start_scr = Starting_screen()
active_scr = start_scr

starting_time = None
ending_time = None
game_duration = None

pregamewait = False
game = None
ultra_game = None

score = 0

enemies_killed = 0
chests_opened = 0
damage_dealt = 0
hp_healed = 0
steps_made = 0

loading = True

hpfont = pygame.font.Font(None, 30)
healordmg_font = pygame.font.Font(None, 50)
game_over_font = pygame.font.Font(None, 150)

keys_used = "WASD"

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        key = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:

            if game:
                if keys_used == "WASD":
                    if key[pygame.K_w]:
                        if game.player_y - 1 in range(0, 8):
                            game.interact(game.player_x, game.player_y - 1, "w")
                    elif key[pygame.K_a]:
                        if game.player_x - 1 in range(0, 8):
                            game.interact(game.player_x - 1, game.player_y, "a")
                    elif key[pygame.K_s]:
                        if game.player_y + 1 in range(0, 8):
                            game.interact(game.player_x, game.player_y + 1, "s")
                    elif key[pygame.K_d]:
                        if game.player_x + 1 in range(0, 8):
                            game.interact(game.player_x + 1, game.player_y, "d")
                elif keys_used == "Arrows":
                    if key[pygame.K_UP]:
                        if game.player_y - 1 in range(0, 8):
                            game.interact(game.player_x, game.player_y - 1, "w")
                    elif key[pygame.K_LEFT]:
                        if game.player_x - 1 in range(0, 8):
                            game.interact(game.player_x - 1, game.player_y, "a")
                    elif key[pygame.K_DOWN]:
                        if game.player_y + 1 in range(0, 8):
                            game.interact(game.player_x, game.player_y + 1, "s")
                    elif key[pygame.K_RIGHT]:
                        if game.player_x + 1 in range(0, 8):
                            game.interact(game.player_x + 1, game.player_y, "d")

                if key[pygame.K_e]:
                    game.attack()
    screen.fill((0, 0, 0))
    active_scr.render(screen)
    pygame.display.flip()
pygame.quit()
