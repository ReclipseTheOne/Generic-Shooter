import json
import pygame as pg
from gslogging import GSLogger
from enum import Enum

FLAGS = pg.DOUBLEBUF | pg.HWSURFACE | pg.RESIZABLE


class Colors(Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    # Star Colors
    PALE_BLUE = (230, 230, 255)
    PALE_YELLOW = (255, 255, 230)
    PALE_PINK = (255, 230, 245)
    PALE_GREEN = (230, 251, 230)



class Fonts(Enum):
    pg.font.init()
    NONE = pg.font.Font(None, 16)
    ROBOTO = pg.font.Font("./resources/fonts/Roboto/Roboto-Regular.ttf", 16)
    ROBOTO_BOLD = pg.font.Font("./resources/fonts/Roboto/Roboto-Bold.ttf", 32)


CONFIG_EXISTS = True
CONFIG = {}

try:
    open("config.json")
except FileNotFoundError:
    GSLogger.error("Config file not found")
    CONFIG_EXISTS = False

if CONFIG_EXISTS:
    with open("config.json", "r") as file:
        CONFIG = json.load(file)
        file.close()

WINDOW_START_WIDTH = CONFIG["window"]["start_width"] if CONFIG_EXISTS else 800
WINDOW_START_HEIGHT = CONFIG["window"]["start_height"] if CONFIG_EXISTS else 600

MAX_ASTEROID_SPEED = CONFIG["asteroid"]["max_speed"] if CONFIG_EXISTS else 3
MIN_ASTEROID_SPEED = CONFIG["asteroid"]["min_speed"] if CONFIG_EXISTS else 1
MAX_ASTEROID_SIZE = CONFIG["asteroid"]["max_size"] if CONFIG_EXISTS else 50
MIN_ASTEROID_SIZE = CONFIG["asteroid"]["min_size"] if CONFIG_EXISTS else 10
MAX_ASTEROID_ROTATION_SPEED = CONFIG["asteroid"]["max_rotation_speed"] if CONFIG_EXISTS else 0.03
MIN_ASTEROID_ROTATION_SPEED = CONFIG["asteroid"]["min_rotation_speed"] if CONFIG_EXISTS else 0.01
ASTEROID_SPAWN_INTERVAL = CONFIG["asteroid"]["spawn_interval"] if CONFIG_EXISTS else 1000

LIVES = CONFIG["gameplay"]["lives"] if CONFIG_EXISTS else 3
TPS = CONFIG["gameplay"]["tps"] if CONFIG_EXISTS else 60
CACHE_SIZE = CONFIG["gameplay"]["cache_size"] if CONFIG_EXISTS else 500


def reload_config():
    global CONFIG_EXISTS, CONFIG, WINDOW_START_WIDTH, WINDOW_START_HEIGHT, MAX_ASTEROID_SPEED, MIN_ASTEROID_SPEED, MAX_ASTEROID_SIZE, MIN_ASTEROID_SIZE, MAX_ASTEROID_ROTATION_SPEED, MIN_ASTEROID_ROTATION_SPEED, TPS, LIVES, CACHE_SIZE, ASTEROID_SPAWN_INTERVAL
    CONFIG_EXISTS = True
    CONFIG = {}

    try:
        open("config.json")
    except FileNotFoundError:
        GSLogger.error("Config file not found")
        CONFIG_EXISTS = False

    if CONFIG_EXISTS:
        with open("config.json", "r") as file:
            CONFIG = json.load(file)
            file.close()

        WINDOW_START_WIDTH = CONFIG["window"]["start_width"]
        WINDOW_START_HEIGHT = CONFIG["window"]["start_height"]
        MAX_ASTEROID_SPEED = CONFIG["asteroid"]["max_speed"]
        MIN_ASTEROID_SPEED = CONFIG["asteroid"]["min_speed"]
        MAX_ASTEROID_SIZE = CONFIG["asteroid"]["max_size"]
        MIN_ASTEROID_SIZE = CONFIG["asteroid"]["min_size"]
        MAX_ASTEROID_ROTATION_SPEED = CONFIG["asteroid"]["max_rotation_speed"]
        MIN_ASTEROID_ROTATION_SPEED = CONFIG["asteroid"]["min_rotation_speed"]
        ASTEROID_SPAWN_INTERVAL = CONFIG["asteroid"]["spawn_interval"]
        LIVES = CONFIG["gameplay"]["lives"]
        TPS = CONFIG["gameplay"]["tps"]
        CACHE_SIZE = CONFIG["gameplay"]["cache_size"]
