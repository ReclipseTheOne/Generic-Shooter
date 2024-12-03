try:
    import pygame as pg
except ImportError:
    print("Import Error >> Please run pip install -r requirements.txt in the folder's workplace")

# Built-in or file imports
import config
from API import Tickable, Drawable, IHitbox
from gslogging import GSLogger
from typing import Union
import random
import time
import math
import util

# Initialization
OBJECTS = []
ASTEROID_SPAWN_SIDE = ["top", "bottom", "left", "right"]
SHOW_HITBOXES = False

cached_window_width = config.WINDOW_START_WIDTH
cached_window_height = config.WINDOW_START_HEIGHT

window_width_multiplier = 1
window_height_multiplier = 1
running = True

if config.CONFIG["debug"] == "True":
    debug = True
else:
    debug = False

# Pygame initialization
gs = pg.init()
pg.display.init()
pg.mixer.init()


GSLogger.info(f"Pygame init: {gs[0]}, {gs[1]}")
CLOCK = pg.time.Clock()
SCREEN = pg.display.set_mode((config.WINDOW_START_WIDTH, config.WINDOW_START_HEIGHT), config.FLAGS)
GSLogger.success("Generic Shooter started successfully")

# Cursor and window settings
pg.display.set_caption("Generic Shooter")
pg.mouse.set_visible(False)


# Classes
class Hitbox(Drawable):
    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.width = x2 - x1
        self.height = y2 - y1

    def is_colliding(self, arg: Union['Hitbox', tuple[float, float]]):
        if isinstance(arg, tuple):
            x, y = arg
            return self.x1 <= x <= self.x2 and self.y1 <= y <= self.y2
        else:
            return self.x1 <= arg.x2 and self.x2 >= arg.x1 and self.y1 <= arg.y2 and self.y2 >= arg.y1

    def draw(self):
        if SHOW_HITBOXES is True:
            pg.draw.rect(SCREEN, (255, 0, 0), (self.x1, self.y1, self.width, self.height))

    def update(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.width = x2 - x1
        self.height = y2 - y1


class Crosshair(Drawable, Tickable):
    def __init__(self):
        self.x = 0
        self.y = 0

    def draw(self):
        pg.draw.line(SCREEN, config.Colors.WHITE.value, (self.x - 10, self.y), (self.x + 10, self.y))
        pg.draw.line(SCREEN, config.Colors.WHITE.value, (self.x, self.y - 10), (self.x, self.y + 10))

    def tick(self):
        self.x, self.y = pg.mouse.get_pos()

    def check_if_hit(self):
        for obj in OBJECTS:
            if isinstance(obj, Asteroid):
                if obj.is_colliding((self.x, self.y)):
                    OBJECTS.remove(obj)
                    SCORECOUNTER.add_score(1)
                    SCORECOUNTER.streak += 1


CROSSHAIR = Crosshair()


class Asteroid(IHitbox, Drawable, Tickable):
    padding = math.floor(SCREEN.get_width() * (config.PADDING / 100))

    def __init__(self):
        self.id = time.time_ns()
        self.speed = random.uniform(config.MIN_ASTEROID_SPEED, config.MAX_ASTEROID_SPEED)
        side = random.choice(ASTEROID_SPAWN_SIDE)
        if side == "top":
            self.x = random.randint(self.padding, SCREEN.get_width() - self.padding)
            self.y = 0
        elif side == "bottom":
            self.x = random.randint(self.padding, SCREEN.get_width() - self.padding)
            self.y = SCREEN.get_height()
        elif side == "left":
            self.x = 0
            self.y = random.randint(self.padding, SCREEN.get_height() - self.padding)
        elif side == "right":
            self.x = SCREEN.get_width()
            self.y = random.randint(self.padding, SCREEN.get_height() - self.padding)

        self.rotation_angle = 0 # in radians

        # Modifiers
        self.size = random.randint(config.MIN_ASTEROID_SIZE, config.MAX_ASTEROID_SIZE)
        self.rotation_speed = random.uniform(config.MIN_ASTEROID_ROTATION_SPEED, config.MAX_ASTEROID_ROTATION_SPEED)

        # Movement
        self.x_modifier = math.floor((self.x / SCREEN.get_width() - 0.5) * 2 * 100) / 100  # -1 to 1 (2 decimal precision) range based on X position, 0 is middle, -1 is left, 1 is right
        self.y_modifier = math.floor((self.y / SCREEN.get_height() - 0.5) * 2 * 100) / 100  # -1 to 1 (2 decimal precision) range based on Y position, 0 is middle, -1 is top, 1 is bottom

        self.vecX = self.speed * abs(self.x_modifier)
        self.vecY = self.speed * abs(self.y_modifier)
        if side == "top":
            pass
        elif side == "bottom":
            self.vecY *= -1
        elif side == "left":
            pass
        elif side == "right":
            self.vecX *= -1

        # Corners
        self.corner_top_right = ((self.x + self.size / 2) * window_width_multiplier, (self.y - self.size / 2) * window_height_multiplier)
        self.corner_top_left = ((self.x - self.size / 2) * window_width_multiplier, ( self.y - self.size / 2) * window_height_multiplier)
        self.corner_bottom_right = ((self.x + self.size / 2) * window_width_multiplier, ( self.y + self.size / 2) * window_height_multiplier)
        self.corner_bottom_left = ((self.x - self.size / 2) * window_width_multiplier, ( self.y + self.size / 2) * window_height_multiplier)

        self._hitbox = Hitbox(
            self.corner_top_left[0],
            self.corner_bottom_right[0],
            self.corner_top_left[1],
            self.corner_bottom_right[1]
        )

    def get_hitbox(self):
        return self._hitbox

    def is_colliding(self, pos: tuple[float, float]):
        return self._hitbox.is_colliding(pos)

    def draw(self):
        pg.draw.polygon(
            SCREEN,
            config.Colors.WHITE.value,
            (
                util.rotate_point(self.corner_top_right[0], self.corner_top_right[1], self.x * window_width_multiplier, self.y * window_height_multiplier, self.rotation_angle),
                util.rotate_point(self.corner_bottom_right[0], self.corner_bottom_right[1], self.x * window_width_multiplier, self.y * window_height_multiplier, self.rotation_angle),
                util.rotate_point(self.corner_bottom_left[0], self.corner_bottom_left[1], self.x * window_width_multiplier, self.y * window_height_multiplier, self.rotation_angle),
                util.rotate_point(self.corner_top_left[0], self.corner_top_left[1], self.x * window_width_multiplier, self.y * window_height_multiplier, self.rotation_angle),
            )
        )

    def tick(self):
        if self.x < -self.size or self.x > SCREEN.get_width() + self.size or self.y < -self.size or self.y > SCREEN.get_height() + self.size:
            OBJECTS.remove(self)
            SCORECOUNTER.lose_life()
        else:
            self.x += self.vecX
            self.y += self.vecY
            self.rotation_angle += self.rotation_speed

            # Update corner positions:
            self.corner_top_right = ((self.x + self.size / 2) * window_width_multiplier, (self.y - self.size / 2) * window_height_multiplier)
            self.corner_top_left = ((self.x - self.size / 2) * window_width_multiplier, (self.y - self.size / 2) * window_height_multiplier)
            self.corner_bottom_right = ((self.x + self.size / 2) * window_width_multiplier, (self.y + self.size / 2) * window_height_multiplier)
            self.corner_bottom_left = ((self.x - self.size / 2) * window_width_multiplier, (self.y + self.size / 2) * window_height_multiplier)

            self._hitbox.update(
                self.corner_top_left[0],
                self.corner_bottom_right[0],
                self.corner_top_left[1],
                self.corner_bottom_right[1]
            )

    def __str__(self):
        return f"Asteroid with ID {self.id}"


    @staticmethod
    def spawn_asteroid(debug=False):
        asteroid = Asteroid()
        OBJECTS.append(asteroid)
        if debug is True:
            GSLogger.debug("Asteroid spawned")


class FPSCounter(Drawable):
    def __init__(self):
        self.fps = 0
        self.show = True
        self.cache = []
        self.ms_cache = []

    def draw(self):
        util.render_text(
            SCREEN,
            f"TPS: {self.fps} - Avg. ms per frame: {self.get_avg()} - Low 1% avg. ms per frame: {self.get_low1perc_avg()} - Set Tick after {math.floor(1000 / config.TPS)}ms", 
            config.Fonts.ROBOTO.value,
            config.Colors.WHITE.value,
            5,
            1
            )

    def update_fps(self, new_fps):
        self.cache.append(self.fps)
        if len(self.cache) > config.CACHE_SIZE:
            self.cache.pop(0)
        self.fps = new_fps

    def get_avg(self):
        if len(self.ms_cache) == 0:
            return 0
        return math.floor(sum(self.ms_cache) / len(self.ms_cache))

    def get_low1perc_avg(self):
        if len(self.ms_cache) == 0:
            return 0
        if len(self.ms_cache) < 101:
            lowest = sorted(self.ms_cache, reverse=True)[0:len(self.ms_cache) - 1]
        else:
            lowest = sorted(self.ms_cache, reverse=True)[0:100]
        if len(lowest) == 0:
            return 0
        return math.floor(sum(lowest) / len(lowest))

    def push_to_ms(self, ms):
        self.ms_cache.append(ms)
        if len(self.ms_cache) > config.CACHE_SIZE:
            self.ms_cache.pop(0)

    def show(self, value):
        self.show = value


FPS_COUNTER = FPSCounter()
OBJECTS.append(FPS_COUNTER)


class ScoreCounter(Drawable):
    def __init__(self):
        self.score = 0
        self.highestscore = 0
        self.streak = 1
        self.lives = config.LIVES
        self.show = True

    def draw(self):
        if self.show is True:
            util.render_text(
                SCREEN,
                f"Lives: {self.lives} - Streak: {self.streak} - Score: {self.score} - Highest: {self.highestscore}",
                config.Fonts.ROBOTO.value,
                config.Colors.WHITE.value,
                5,
                20
            )

    def add_score(self, score):
        self.score += score * self.streak
        if self.score > self.highestscore:
            self.highestscore = self.score

    def reset(self):
        DAMAGE_SCREEN.damage(2)

        self.score = 0
        self.lives = config.LIVES
        SPAWNING.is_enabled = False

        global OBJECTS
        OBJECTS = util.clear_list_of(OBJECTS, Asteroid)

        SPAWNING.asteroid_spawn_interval = config.ASTEROID_SPAWN_INTERVAL

    def lose_life(self):
        self.lives -= 1
        self.streak = 1

        DAMAGE_SCREEN.damage()

        if self.lives == 0:
            self.reset()

    def show(self, value):
        self.show = value



SCORECOUNTER = ScoreCounter()
OBJECTS.append(SCORECOUNTER)


class Star(Drawable, Tickable):
    def __init__(self, y=0):
        self.x = random.randint(0, SCREEN.get_width())
        self.y = y
        self.y_speed = random.uniform(0.3, 0.7)
        self.color = random.choice(
            [config.Colors.PALE_BLUE.value,
             config.Colors.PALE_YELLOW.value,
             config.Colors.PALE_PINK.value,
             config.Colors.PALE_GREEN.value]
        )

    def draw(self):
        pg.draw.rect(
            SCREEN,
            self.color,
            (
                self.x * window_width_multiplier,
                self.y * window_height_multiplier,
                1,
                1
            )
        )

    def tick(self):
        if self.y > SCREEN.get_height():
            OBJECTS.remove(self)
        self.y += self.y_speed


# Initial decoration stars
for i in range(1, config.WINDOW_START_HEIGHT):
    for j in range(1, random.randint(1, 4)):
        star = Star(i)
        OBJECTS.append(star)


class Spawning(Tickable):
    def __init__(self):
        self.asteroid_time_stamp = time.time_ns() / 1_000_000 # in ms
        self.asteroid_spawn_interval = config.ASTEROID_SPAWN_INTERVAL
        self.is_enabled = False

    @staticmethod
    def now():  # in ms
        return time.time_ns() / 1_000_000

    def is_enabled(self, enabled):
        self.is_enabled = enabled

    def tick(self):
        now = Spawning.now()

        if self.is_enabled is True:
            # Asteroid Spawning
            if now - self.asteroid_time_stamp > 1000 + self.asteroid_spawn_interval:
                for i in range(1, random.randint(1, 5)):
                    Asteroid.spawn_asteroid()
                self.asteroid_spawn_interval *= random.uniform(0.92, 0.99)
                self.asteroid_time_stamp = now


SPAWNING = Spawning()
OBJECTS.append(SPAWNING)


class DamageScreen(Drawable):
    dmg_surface = pg.Surface((SCREEN.get_width(), SCREEN.get_height()))

    def __init__(self, surface: pg.Surface):
        self.surface = surface
        self.alpha = 0
        self.color = (255, 0, 0)

    def draw(self):
        # GSLogger.info("Drawing damage screen at alpha: " + str(self.alpha))
        if self.alpha >= 0:
            self.dmg_surface.set_alpha(self.alpha)
            self.dmg_surface.fill(self.color)
            self.surface.blit(self.dmg_surface, (0, 0))

            self.alpha = self.alpha - 1

    def damage(self, multiplier=1):
        if (multiplier > 2):
            multiplier = 2
        self.alpha = 90 * multiplier

DAMAGE_SCREEN = DamageScreen(SCREEN)
OBJECTS.append(DAMAGE_SCREEN)

# Event Binding
def key_press(event: pg.event.Event):
    if event.type == pg.KEYDOWN:
        if event.key == pg.K_ESCAPE:
            global running
            running = False

            pg.quit()
            GSLogger.success("Generic Shooter stopped successfully")

        elif event.key == pg.K_e:
            if SPAWNING.is_enabled is True:
                SPAWNING.is_enabled = False
                GSLogger.debug("Spawning disabled")
            else:
                SPAWNING.is_enabled = True
                GSLogger.debug("Spawning enabled")

        elif event.key == pg.K_a:
            Asteroid.spawn_asteroid()

        elif event.key == pg.K_c:
            global OBJECTS
            OBJECTS = util.clear_list_of(OBJECTS, Asteroid)
            if debug is True:
                GSLogger.debug("Asteroid cleared")
        elif event.key == pg.K_SPACE:
            CROSSHAIR.check_if_hit()

        elif event.key == pg.K_h:
            global SHOW_HITBOXES
            if SHOW_HITBOXES is True:
                GSLogger.debug("Hitboxes hidden")
            else:
                GSLogger.debug("Hitboxes shown")
            SHOW_HITBOXES = not SHOW_HITBOXES


# Runtime
while running:
    # Event Handling
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            key_press(event)

    # Drawing and ticking
    SCREEN.fill(config.Colors.BLACK.value)
    for obj in OBJECTS:
        if isinstance(obj, Drawable):
            obj.draw()
        if isinstance(obj, Tickable):
            obj.tick() 
        if isinstance(obj, IHitbox):
            obj.get_hitbox().draw()

    # Put CROSSHAIR on top Z-Index
    CROSSHAIR.tick()
    CROSSHAIR.draw()

    # Multiply calculation and rendering by how much the window has been resized
    window_height_multiplier = SCREEN.get_height() / config.WINDOW_START_HEIGHT 
    window_width_multiplier = SCREEN.get_width() / config.WINDOW_START_WIDTH

    if cached_window_width != SCREEN.get_width() or cached_window_height != SCREEN.get_height():
        if debug is True:
            GSLogger.debug("Window resized")
            GSLogger.debug(f"Window width multiplier: {window_width_multiplier}")
            GSLogger.debug(f"Window height multiplier: {window_height_multiplier}")
            GSLogger.debug(f"Window width: {SCREEN.get_width()} - Prev: {cached_window_width} Start: {config.WINDOW_START_WIDTH} ")
            GSLogger.debug(f"Window height: {SCREEN.get_height()} - Prev: {cached_window_height} - Start: {config.WINDOW_START_HEIGHT}")
            cached_window_height = SCREEN.get_height()
            cached_window_width = SCREEN.get_width()

    # Spawn decoration stars
    for i in range(1, random.randint(1, 4)):
        star = Star()
        OBJECTS.append(star)

    # Timing the frame time
    __fps_timestamp_start = time.time_ns()
    pg.display.update()
    CLOCK.tick(config.TPS)
    __fps_timestamp_end = time.time_ns()

    time_diff_ns = __fps_timestamp_end - __fps_timestamp_start
    # GSLogger.debug(f"Frame time: {time_diff_ns / 1_000_000}ms")
    if time_diff_ns > 0:
        FPS_COUNTER.update_fps(math.floor(1_000_000_000 / time_diff_ns))
        FPS_COUNTER.push_to_ms(time_diff_ns / 1_000_000)
    else:
        FPS_COUNTER.update_fps(0)

pg.quit()