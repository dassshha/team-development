import os
import pygame
import random
import sys

from Main_platform import MainPlatform
from Mark import Mario
from Objects import Mob, MobGumba, MobBonus, MobMushroom
from Start import Start, Settings, Info, Match, Reload, Exit, Heart, Quit, Next, Finish, Clouds

x_fin = 400


class Camera:  # камера для движения поля
    def __init__(self):
        self.dx = 0
        self.dy = 0
        self.dash = 0

    def apply(self, obj):
        obj.rect.x += self.dx

    def update(self, sp):
        self.mario_vekt = sp[0]
        self.mario_x = sp[1]
        if self.mario_x >= 250:
            if self.mario_vekt == 1:
                self.dx = -8
                self.dash = 8
            elif self.mario_vekt == -1:
                self.dx = 8
                self.dash = -8
        else:
            self.dx = 0
            self.dash = mario.get_dash()

    def get_lent(self):
        return self.dash


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


LENTH = 5000  # длина уровня по умолчанию
LIFES = 3  # количество жизней
WIDTH, HEIGHT = 700, 600  # размер поля
running = True
FPS = 30  # частота кадров
fps_cahnge = 0
wons = 0


def start_screen(LENTH):  # начальный экран + вкладка "авторы" + вкладка "выбор сложности"
    fon = pygame.transform.scale(load_image('start_screen.jpg'), (WIDTH, HEIGHT))
    pygame.init()
    writer = False
    wix = False
    mn1 = []
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Добро пожаловать !')
    image = load_image("mario_start.png")
    pygame.display.set_icon(image)
    clock = pygame.time.Clock()
    screen.blit(fon, (0, 0))
    all_sp = pygame.sprite.Group()
    msp = pygame.sprite.Group()
    play_but = Start(all_sp)
    inf_but = Info(all_sp)
    set_but = Settings(all_sp)
    mn = [play_but, inf_but, set_but]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                zn = True
                for el in mn:
                    if el.vekt == 3:
                        zn = False
                if zn:
                    for el in mn:
                        x, y = event.pos
                        el.is_on(x, y)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if play_but.click(x, y) and play_but.vekt != 3:
                    for el in mn:
                        el.vekt = 3
                    return LENTH
                elif inf_but.click(x, y) and inf_but.vekt != 3:
                    for el in mn:
                        el.vekt = 3
                    writer = True
                elif set_but.click(x, y) and set_but.vekt != 3:
                    for el in mn:
                        el.vekt = 3
                    wix = True
                    for i in range(1, 4):
                        mn1.append(Match(i, LENTH))
                    for el in mn1:
                        el.set_gr(msp)
                c = 0
                for el in mn1:
                    if el.k == 0:
                        c += 1
                if c == 3:
                    for el in mn1:
                        st = el.click(x, y)
                        if st == 'done':
                            el.set_dot()
                            if el.i == 1:
                                LENTH = 5000
                            elif el.i == 2:
                                LENTH = 30000
                            elif el.i == 3:
                                LENTH = 50000
                            for el1 in mn1:
                                if el != el1:
                                    el1.del_dot()
            elif event.type == pygame.KEYDOWN:
                zn = True
                if event.key == pygame.K_ESCAPE:
                    for el in mn:
                        if el.vekt == 3:
                            pass
                        else:
                            zn = False
                    if zn:
                        for el in mn:
                            el.vekt = 0
                    writer = False
                    wix = False
                    for el in mn1:
                        el.clear()

        all_sp.update()
        screen.blit(fon, (0, 0))
        all_sp.draw(screen)
        msp.draw(screen)
        if writer:
            intro_text = ["                         Авторы:", "", "",
                          "  Жгулёва Дарья    Дикобаева Анастасия"]
            font = pygame.font.Font('Data/Mario_font.ttf', 12)
            text_coord = 230
            for line in intro_text:
                string_rendered = font.render(line, 4, pygame.Color('yellow'))
                intro_rect = string_rendered.get_rect()
                text_coord += 10
                intro_rect.top = text_coord
                intro_rect.x = 10
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
            intro_text = ["Press esc to leave"]
            font = pygame.font.Font('Data/Mario_font.ttf', 8)
            text_coord = 230
            for line in intro_text:
                string_rendered = font.render(line, 4, pygame.Color('blue'))
                intro_rect = string_rendered.get_rect()
                text_coord += 10
                intro_rect.top = HEIGHT - 25
                intro_rect.x = 10
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
        elif wix:
            intro_text = ["             Выберите cложность :", "", "",
                          "                            Лёгкая",
                          "", "", "", "", "",
                          "                            Средняя",
                          "", "", "", "", "",
                          "                            Хард"]
            font = pygame.font.Font('Data/Mario_font.ttf', 15)
            text_coord = 75
            for line in intro_text:
                string_rendered = font.render(line, 1, (100, 0, 0))
                intro_rect = string_rendered.get_rect()
                text_coord += 10
                intro_rect.top = text_coord
                intro_rect.x = 10
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
            intro_text = ["Press esc to leave"]
            font = pygame.font.Font('Data/Mario_font.ttf', 8)
            text_coord = 230
            for line in intro_text:
                string_rendered = font.render(line, 4, pygame.Color('blue'))
                intro_rect = string_rendered.get_rect()
                text_coord += 10
                intro_rect.top = HEIGHT - 25
                intro_rect.x = 10
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
        pygame.display.flip()
        clock.tick(30)


def lost(fps):  # проигрыш
    pygame.init()
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Mario ultra 2021')
    image = load_image("mario_start.png")
    pygame.display.set_icon(image)
    fps_cahnge = fps
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            zn = True
            for el in mn:
                if el.vekt == 3:
                    zn = False
            if zn:
                for el in mn:
                    x, y = event.pos
                    el.is_on(x, y)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if reload_but.click(x, y) and reload_but.vekt != 3:
                for el in mn:
                    el.vekt = 3
                return 3
            elif exit_but.click(x, y) and exit_but.vekt != 3:
                for el in mn:
                    el.vekt = 3
                print("U just can't win...")
                pygame.quit()
                sys.exit()
    screen.fill((0, 0, 0))
    if LENTH <= 5000:
        screen.blit(load_image("fon_level1.png"), (0, 0))
    elif LENTH == 30000:
        screen.blit(load_image("fon_level2.jpg"), (0, 0))
    elif LENTH >= 50000:
        screen.blit(load_image("fon_level3.png"), (0, 0))
    mob_sprites.draw(screen)
    all_sprites.draw(screen)
    entities.draw(screen)
    if fps_cahnge == 1:
        image_lost = load_image('game_over.png')
        screen.blit(image_lost, (0, 0))
    elif fps_cahnge == 2:
        image_lost1 = load_image('game_over1.png')
        screen.blit(image_lost1, (0, 0))
    elif fps_cahnge == 3:
        image_lost1 = load_image('game_over2.png')
        screen.blit(image_lost1, (0, 0))
    button_end_sprites.update()
    button_end_sprites.draw(screen)
    image = load_image("mario_start.png")
    pygame.display.set_icon(image)
    clock.tick(10)
    pygame.display.flip()
    return 0