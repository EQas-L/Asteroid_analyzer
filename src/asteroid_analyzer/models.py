from dataclasses import dataclass
from enum import Enum


class SpriteType(Enum):
    PLAYER = "Player"
    ASTEROID = "Asteroid"
    SHOT = "Shot"
    ASTEROID_FIELD = "AsteroidField"


@dataclass(frozen=True, slots=True)
class Vec2:
    x: float
    y: float


@dataclass(frozen=True, slots=True)
class Size:
    height: int
    width: int

    @property
    def area(self) -> int:
        return self.width * self.height


@dataclass(frozen=True, slots=True)
class Sprite:
    id: int
    type: SpriteType
    position: Vec2
    velocity: Vec2
    radius: float
    rotation: float | None = None


@dataclass(frozen=True, slots=True)
class Snapshot:
    v: int
    timestamp: str
    elapsed_s: int
    frame: int
    screen: Size
    sprites: tuple[Sprite, ...]
