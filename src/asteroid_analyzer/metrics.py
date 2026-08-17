from collections import Counter
from dataclasses import dataclass
from math import pi

from .models import Snapshot, SpriteType


@dataclass(slots=True)
class ObjectLife:
    id: int
    sprite_type: SpriteType
    first_frame: int
    last_frame: int


@dataclass(frozen=True, slots=True)
class Report:
    asteroid_area_fraction: list[float]
    sprites_on_screen: list[int]
    sprites_appearance_by_type: dict[SpriteType, int]
    asteroids_destroyed: int
    shots_hit_fraction: float
    objects_life_time: dict[int, tuple[int, SpriteType]]  # id -> life time in frames
    survived_asteroid: int
    survived_shots: int
    objects_life: dict[int, ObjectLife]

    @property
    def max_sprites(self) -> int:
        if self.sprites_on_screen:
            return max(self.sprites_on_screen)
        else:
            return 0

    @property
    def average_sprites(self) -> float:
        if self.sprites_on_screen:
            return round(sum(self.sprites_on_screen) / len(self.sprites_on_screen), 3)
        else:
            return 0

    @property
    def max_fraction(self) -> float:
        if self.asteroid_area_fraction:
            return round(max(self.asteroid_area_fraction), 3)
        else:
            return 0

    @property
    def average_fraction(self) -> float:
        if self.asteroid_area_fraction:
            return round(sum(self.asteroid_area_fraction) / len(self.asteroid_area_fraction), 3)
        else:
            return 0

    @property
    def average_life_time_asteroids(self) -> float:
        sm = sum(
            life_time
            for life_time, sprite_type in self.objects_life_time.values()
            if sprite_type is SpriteType.ASTEROID
        )
        ln = sum(
            1
            for _, sprite_type in self.objects_life_time.values()
            if sprite_type is SpriteType.ASTEROID
        )
        if ln > 0:
            return round(sm / ln, 3)
        else:
            return 0

    @property
    def average_life_time_shots(self) -> float:
        sm = sum(
            life_time
            for life_time, sprite_type in self.objects_life_time.values()
            if sprite_type is SpriteType.SHOT
        )
        ln = sum(
            1
            for _, sprite_type in self.objects_life_time.values()
            if sprite_type is SpriteType.SHOT
        )
        if ln > 0:
            return round(sm / ln, 3)
        else:
            return 0


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
        area = 0.0
        on_screen = 0
        for sprite in snapshot.sprites:
            if sprite.id not in self.objects_life:
                self.objects_life[sprite.id] = ObjectLife(
                    id=sprite.id,
                    sprite_type=sprite.type,
                    first_frame=snapshot.frame,
                    last_frame=snapshot.frame,
                )
            else:
                self.objects_life[sprite.id].last_frame = snapshot.frame

            if (
                0 <= sprite.position.y <= snapshot.screen.height
                and 0 <= sprite.position.x <= snapshot.screen.width
            ):
                if sprite.type is SpriteType.ASTEROID:
                    area += sprite.radius**2 * pi
                on_screen += 1
                self.sprites_appearance_by_type.update([sprite.type])

        self.asteroid_area_fraction.append(area / snapshot.screen.area)
        self.sprites_on_screen.append(on_screen)
        self.snapshots_total += 1

    def report(self) -> Report:
        total_shots = 0
        objects_life_time: dict[int, tuple[int, SpriteType]] = {}
        asteroids_destroyed = 0
        shots_hit = 0
        survived_asteroid = 0
        survived_shots = 0
        for obj in self.objects_life.values():
            if obj.last_frame != self.last_frame:
                objects_life_time[obj.id] = (obj.last_frame - obj.first_frame, obj.sprite_type)
            if obj.sprite_type is SpriteType.ASTEROID:
                if obj.last_frame != self.last_frame:
                    asteroids_destroyed += 1
                else:
                    survived_asteroid += 1
            elif obj.sprite_type is SpriteType.SHOT:
                total_shots += 1
                if obj.last_frame != self.last_frame:
                    shots_hit += 1
                else:
                    survived_shots += 1

        return Report(
            asteroid_area_fraction=self.asteroid_area_fraction,
            sprites_on_screen=self.sprites_on_screen,
            sprites_appearance_by_type=dict(self.sprites_appearance_by_type),
            asteroids_destroyed=asteroids_destroyed,
            shots_hit_fraction=shots_hit / max(1, total_shots),
            objects_life_time=objects_life_time,
            survived_asteroid=survived_asteroid,
            survived_shots=survived_shots,
            objects_life=self.objects_life,
        )
