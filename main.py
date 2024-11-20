try:
    import tkinter as tk
except ImportError:
    print("Import Error >> Please run pip install -r requirements.txt in the folder's workplace")

# Built-in or file imports
import config
from API import Tickable, Drawable
from gslogging import GSLogger
import random
import time
import math
import util

# Initialization
OBJECTS = []
ASTEROID_SPAWN_SIDE = ["top", "bottom", "left", "right"]

window_width_multiplier = 1
window_height_multiplier = 1
running = True
if config.CONFIG["debug"] == "True":
    debug = True
else:
    debug = False

GenericShooter = tk.Tk()
GenericShooter.title("Generic Shooter")
GenericShooter.geometry(f"{config.WINDOW_START_WIDTH}x{config.WINDOW_START_HEIGHT}")
GenericShooter.config(cursor="none")

GSCanvas = tk.Canvas(GenericShooter, bg="black", bd=0, highlightthickness=0)
GSCanvas.pack(fill=tk.BOTH, expand=True)
GSLogger.success("Generic Shooter started successfully")


# Classes
class Crosshair(Drawable):
    def __init__(self):
        self.x = 0
        self.y = 0

    def draw(self):
        GSCanvas.delete("crosshair_line_1")
        GSCanvas.delete("crosshair_line_2")
        GSCanvas.create_line(self.x - 10, self.y, self.x + 10, self.y, fill="white", tags="crosshair_line_1")
        GSCanvas.create_line(self.x, self.y - 10, self.x, self.y + 10, fill="white", tags="crosshair_line_2")

    def update_pos(self, event):
        self.x = event.x
        self.y = event.y


CROSSHAIR = Crosshair()
OBJECTS.append(CROSSHAIR)


class Asteroid(Drawable, Tickable):
    def __init__(self):
        self.id = time.time_ns()
        side = random.choice(ASTEROID_SPAWN_SIDE)
        if side == "top":
            self.x = random.randint(0, GenericShooter.winfo_width())
            self.y = 0
        elif side == "bottom":
            self.x = random.randint(0, GenericShooter.winfo_width())
            self.y = GenericShooter.winfo_height()
        elif side == "left":
            self.x = 0
            self.y = random.randint(0, GenericShooter.winfo_height())
        elif side == "right":
            self.x = GenericShooter.winfo_width()
            self.y = random.randint(0, GenericShooter.winfo_height())
        
        self.rotation_angle = 0 # in radians

        # Modifiers
        self.size = random.randint(config.MIN_ASTEROID_SIZE, config.MAX_ASTEROID_SIZE)
        self.rotation_speed = random.uniform(config.MIN_ASTEROID_ROTATION_SPEED, config.MAX_ASTEROID_ROTATION_SPEED)
        
        # Movement
        self.vecX = random.uniform(config.MIN_ASTEROID_SPEED, config.MAX_ASTEROID_SPEED)
        self.vecY = random.uniform(config.MIN_ASTEROID_SPEED, config.MAX_ASTEROID_SPEED)
        if side == "top":
            pass
        elif side == "bottom":
            self.vecY *= -1
        elif side == "left":
            pass
        elif side == "right":
            self.vecX *= -1

        # Corners
        self.corner_top_right = (self.x + self.size / 2, self.y - self.size / 2)
        self.corner_top_left = (self.x - self.size / 2, self.y - self.size / 2)
        self.corner_bottom_right = (self.x + self.size / 2, self.y + self.size / 2)
        self.corner_bottom_left = (self.x - self.size / 2, self.y + self.size / 2)
    
    def draw(self):
        GSCanvas.delete(f"asteroid_{self.id}")
        GSCanvas.create_polygon(
            util.rotate_point(self.corner_top_right[0], self.corner_top_right[1], self.x, self.y, self.rotation_angle),
            util.rotate_point(self.corner_bottom_right[0], self.corner_bottom_right[1], self.x, self.y, self.rotation_angle),
            util.rotate_point(self.corner_bottom_left[0], self.corner_bottom_left[1], self.x, self.y, self.rotation_angle),
            util.rotate_point(self.corner_top_left[0], self.corner_top_left[1], self.x, self.y, self.rotation_angle),
            fill="white",
            tags=f"asteroid_{self.id}"
        )

    def tick(self):
        if self.x < 0 or self.x > GenericShooter.winfo_width() or self.y < 0 or self.y > GenericShooter.winfo_height():
            OBJECTS.remove(self)
            GSCanvas.delete(f"asteroid_{self.id}")
        else:
            self.x += self.vecX
            self.y += self.vecY
            self.rotation_angle += self.rotation_speed
            
            # Update corner positions:
            self.corner_top_right = (self.x + self.size / 2, self.y - self.size / 2)
            self.corner_top_left = (self.x - self.size / 2, self.y - self.size / 2)
            self.corner_bottom_right = (self.x + self.size / 2, self.y + self.size / 2)
            self.corner_bottom_left = (self.x - self.size / 2, self.y + self.size / 2)

    @staticmethod
    def spawn_asteroid(debug=False):
        asteroid = Asteroid()
        OBJECTS.append(asteroid)
        if debug is True:
            GSLogger.debug("Asteroid spawned")


class FPSCounter(Drawable):
    def __init__(self):
        self.fps = 0
        self.cache = []
        self.ms_cache = []

    def draw(self):
        GSCanvas.delete("fps")
        GSCanvas.create_text(225, 10, text=f"TPS: {self.fps} - Avg. ms per frame: {self.get_avg()} - Low 1% avg. ms per frame: {self.get_low1perc_avg()} - Set Tick after {math.floor(1000 / config.TPS)}ms", fill="white", tags="fps")

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
            lowest = sorted(self.ms_cache)[0:len(self.ms_cache) - 1]
        else:
            lowest = sorted(self.ms_cache)[0:100]
        if len(lowest) == 0:
            return 0
        return math.floor(sum(lowest) / len(lowest))
    
    def push_to_ms(self, ms):
        self.ms_cache.append(ms)
        if len(self.ms_cache) > config.CACHE_SIZE:
            self.ms_cache.pop(0)


FPS_COUNTER = FPSCounter()
OBJECTS.append(FPS_COUNTER)


# Event Binding
def key_press(event):
    if event.keysym == "Escape":
        global running
        running = False
        GenericShooter.destroy()
        GSLogger.success("Generic Shooter stopped successfully")
    elif event.keysym == "a":
        Asteroid.spawn_asteroid()
    elif event.keysym == "c":
        for obj in OBJECTS:
            if isinstance(obj, Asteroid):
                OBJECTS.remove(obj)
                if debug is True:
                    GSLogger.debug("Asteroid cleared")


def key_release(event):
    pass


GenericShooter.bind("<KeyPress>", key_press)
GenericShooter.bind("<KeyRelease>", key_release)
GenericShooter.bind("<Motion>", CROSSHAIR.update_pos)


# Runtime
while running:
    for obj in OBJECTS:
        if isinstance(obj, Drawable):
            obj.draw()
        if isinstance(obj, Tickable):
            obj.tick() 

    # Multiply calculation and rendering by how much the window has been resized
    window_height_multiplier = GenericShooter.winfo_height() / config.WINDOW_START_HEIGHT 
    window_width_multiplier = GenericShooter.winfo_width() / config.WINDOW_START_WIDTH

    __fps_timestamp_start = time.time_ns()
    GenericShooter.after(math.floor(1000 / config.TPS))
    GenericShooter.update()
    __fps_timestamp_end = time.time_ns()

    time_diff_ns = __fps_timestamp_end - __fps_timestamp_start
    if time_diff_ns > 0:
        FPS_COUNTER.update_fps(math.floor(1_000_000_000 / time_diff_ns))
        FPS_COUNTER.push_to_ms(time_diff_ns / 1_000_000)
    else:
        FPS_COUNTER.update_fps(0)

GenericShooter.mainloop()