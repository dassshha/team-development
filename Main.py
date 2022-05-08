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

