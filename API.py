from abc import abstractmethod, ABC


class Hitbox:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def get_hitbox(self) -> tuple:
        return self.x, self.y, self.width, self.height

    def is_colliding(self, hitbox) -> bool:
        return self.x < hitbox.x + hitbox.width and self.x + self.width > hitbox.x and self.y < hitbox.y + hitbox.height and self.y + self.height > hitbox.y


class Tickable(ABC):
    @abstractmethod
    def tick(self):
        # Implement any logic that should run on window update
        pass


class Drawable(ABC):
    @abstractmethod
    def draw(self):
        # Implement any logic that should run on window draw
        pass


class IHitbox(ABC):
    @abstractmethod
    def get_hitbox(self) -> Hitbox:
        # Return the hitbox of the object
        pass

    def is_colliding(self, hitbox: Hitbox) -> bool:
        # Return if the object is colliding with the hitbox of another object
        pass