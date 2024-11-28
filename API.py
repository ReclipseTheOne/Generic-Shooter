from abc import abstractmethod, ABC


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
    def is_colliding(self, x, y) -> bool:
        # Return if the coords are inside it's hitbox
        pass