from collections import Counter
from dataclasses import dataclass
from math import pi

from models import Snapshot, SpriteType


@dataclass(slots=True)
class ObjectLife:
    id : int
    sprite_type: SpriteType
    first_frame: int
    last_frame: int

@dataclass(frozen=True, slots=True)
class Report:
    asteroid_area_fraction: list[float]
    sprites_on_screen: list[int]
    sprites_appearance_by_type: dict[str, int]
    asteroids_destroyed: int
    percent_shots_hit: float
    objects_life_time: dict[int, int] # id -> life time in frames
    survived: list[int]

class MetricsCollector:

    def __init__(self) -> None:
        self.asteroid_area_fraction: list[float] = []
        self.sprites_on_screen: list[int] = []
        self.sprites_appearance_by_type: Counter[SpriteType] = Counter()
        self.objects_life: dict[int, ObjectLife] = {}
        self.snapshots_total: int = 0
        self.last_frame: int = 0

    def update(self, snapshot: Snapshot) -> None:
        self.last_frame = snapshot.frame
        area = 0
        on_screen = 0
        for sprite in snapshot.sprites:
            if sprite.id not in self.objects_life:
                self.objects_life[sprite.id] = ObjectLife(
                    id = sprite.id,
                    sprite_type = sprite.type,
                    first_frame = snapshot.frame,
                    last_frame = snapshot.frame
                )
            else:
                self.objects_life[sprite.id].last_frame = snapshot.frame

            if 0 <= sprite.position.y <= snapshot.screen.height and 0 <= sprite.position.x <= snapshot.screen.width:
                if sprite.type is SpriteType.ASTEROID:
                    area += sprite.radius ** 2 * pi
                on_screen += 1
                self.sprites_appearance_by_type.update([sprite.type])

        self.asteroid_area_fraction.append(area / snapshot.screen.area)
        self.sprites_on_screen.append(on_screen)
        self.snapshots_total += 1

    def report(self) -> Report:
        total_shots = 0
        objects_life_time: dict[int, int | str] = {}
        asteroids_destroyed = 0
        shots_hit = 0
        survived = []
        for obj in self.objects_life.values():
            if obj.last_frame  != self.last_frame:
                objects_life_time[obj.id] = obj.last_frame - obj.first_frame
            else:
                survived.append(obj.id)
            if obj.sprite_type is SpriteType.ASTEROID:
                if obj.last_frame  != self.last_frame:
                    asteroids_destroyed += 1
            elif obj.sprite_type is SpriteType.SHOT:
                total_shots += 1
                if obj.last_frame  != self.last_frame:
                    shots_hit += 1
        return Report(
            asteroid_area_fraction=self.asteroid_area_fraction,
            sprites_on_screen=self.sprites_on_screen,
            sprites_appearance_by_type=dict(self.sprites_appearance_by_type),
            asteroids_destroyed=asteroids_destroyed,
            percent_shots_hit=shots_hit / max(1, total_shots),
            objects_life_time=objects_life_time,
            survived=survived
        )


