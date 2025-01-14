import pygame as pg
import random
import time

pg.mixer.init()
sfx = pg.mixer.Sound


def getExplosionSound() -> pg.mixer.Sound:
    explosions = [sfx(".\\resources\\sounds\\explosion 1.wav"), sfx(".\\resources\\sounds\\explosion 2.wav"), sfx(".\\resources\\sounds\\explosion 3.wav")]
    return random.choice(explosions)


HURT = sfx(".\\resources\\sounds\\hurt.wav")
RESET_LIFE = sfx(".\\resources\\sounds\\hurt big.wav")

LASER = sfx(".\\resources\\sounds\\laser.wav")

last_music: pg.mixer.Sound = None
def getBackgroundMusic() -> pg.mixer.Sound:
    global last_music
    BACKGROUND_MUSIC: pg.mixer.Sound = [sfx(".\\resources\\sounds\\Pix - A Green Pig.mp3"), sfx(".\\resources\\sounds\\Pix - Punky Troll.mp3"), sfx(".\\resources\\sounds\\Pix - Space Travel.mp3")]
    new_music = random.choice(BACKGROUND_MUSIC)
    while new_music == last_music:
        new_music = random.choice(BACKGROUND_MUSIC)
    last_music = new_music
    return new_music
