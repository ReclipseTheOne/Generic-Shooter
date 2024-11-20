import json
from gslogging import GSLogger

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

LIVES = CONFIG["gameplay"]["lives"] if CONFIG_EXISTS else 3
TPS = CONFIG["gameplay"]["tps"] if CONFIG_EXISTS else 60
CACHE_SIZE = CONFIG["gameplay"]["cache_size"] if CONFIG_EXISTS else 500


def reload_config():
    global CONFIG_EXISTS, CONFIG, WINDOW_START_WIDTH, WINDOW_START_HEIGHT, MAX_ASTEROID_SPEED, MIN_ASTEROID_SPEED, MAX_ASTEROID_SIZE, MIN_ASTEROID_SIZE, MAX_ASTEROID_ROTATION_SPEED, MIN_ASTEROID_ROTATION_SPEED, TPS, LIVES, CACHE_SIZE
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
        LIVES = CONFIG["gameplay"]["lives"]
        TPS = CONFIG["gameplay"]["tps"]
        CACHE_SIZE = CONFIG["gameplay"]["cache_size"]
