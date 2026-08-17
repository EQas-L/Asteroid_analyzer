from asteroid_analyzer.metrics import MetricsCollector
from asteroid_analyzer.models import Size, Snapshot, Sprite, SpriteType, Vec2

SNAPSHOT = Snapshot(
    v=2,
    timestamp="11:35:52.480",
    elapsed_s=1,
    frame=60,
    screen=Size(height=720, width=1280),
    sprites=(
        Sprite(
            id=1,
            type=SpriteType.PLAYER,
            position=Vec2(652.68, 361.27),
            velocity=Vec2(0.0, 0.0),
            radius=20.0,
            rotation=-91.5,
        ),
        Sprite(
            id=2,
            type=SpriteType.ASTEROID,
            position=Vec2(1207.84, 687.1),
            velocity=Vec2(21.5, -74.98),
            radius=20.0,
        ),
        Sprite(
            id=3,
            type=SpriteType.ASTEROID,
            position=Vec2(1207.84, 687.1),
            velocity=Vec2(21.5, -74.98),
            radius=20.0,
        ),
        Sprite(
            id=4,
            type=SpriteType.SHOT,
            position=Vec2(1249.4, 542.17),
            velocity=Vec2(21.5, -74.98),
            radius=5,
        ),
        Sprite(
            id=5,
            type=SpriteType.SHOT,
            position=Vec2(1249.4, 542.17),
            velocity=Vec2(21.5, -74.98),
            radius=5,
        ),
        Sprite(
            id=6,
            type=SpriteType.ASTEROID,
            position=Vec2(1207.84, 687.1),
            velocity=Vec2(21.5, -74.98),
            radius=20.0,
        ),
    ),
)

SNAPSHOT2 = Snapshot(
    v=2,
    timestamp="11:35:53.445",
    elapsed_s=2,
    frame=120,
    screen=Size(height=720, width=1280),
    sprites=(
        Sprite(
            id=1,
            type=SpriteType.PLAYER,
            position=Vec2(652.68, 361.27),
            velocity=Vec2(0.0, 0.0),
            radius=20.0,
            rotation=-91.5,
        ),
        Sprite(
            id=3,
            type=SpriteType.ASTEROID,
            position=Vec2(1207.84, 687.1),
            velocity=Vec2(21.5, -74.98),
            radius=20.0,
        ),
        Sprite(
            id=4,
            type=SpriteType.SHOT,
            position=Vec2(1249.4, 542.17),
            velocity=Vec2(21.5, -74.98),
            radius=5,
        ),
        Sprite(
            id=6,
            type=SpriteType.ASTEROID,
            position=Vec2(1207.84, 687.1),
            velocity=Vec2(21.5, -74.98),
            radius=20.0,
        ),
    ),
)

SNAPSHOT3 = Snapshot(
    v=2,
    timestamp="11:35:54.445",
    elapsed_s=3,
    frame=180,
    screen=Size(height=720, width=1280),
    sprites=(
        Sprite(
            id=1,
            type=SpriteType.PLAYER,
            position=Vec2(652.68, 361.27),
            velocity=Vec2(0.0, 0.0),
            radius=20.0,
            rotation=-91.5,
        ),
        Sprite(
            id=3,
            type=SpriteType.ASTEROID,
            position=Vec2(1207.84, 687.1),
            velocity=Vec2(21.5, -74.98),
            radius=20.0,
        ),
        Sprite(
            id=4,
            type=SpriteType.SHOT,
            position=Vec2(1249.4, 542.17),
            velocity=Vec2(21.5, -74.98),
            radius=5,
        ),
        Sprite(
            id=6,
            type=SpriteType.ASTEROID,
            position=Vec2(1207.84, 687.1),
            velocity=Vec2(21.5, -74.98),
            radius=20.0,
        ),
    ),
)


Snapshots = [SNAPSHOT, SNAPSHOT2, SNAPSHOT3]


def test_MetricsCollector() -> None:
    collector = MetricsCollector()
    for snapshot in Snapshots:
        collector.update(snapshot)

    report = collector.report()
    assert report.shots_hit_fraction == 0.5
    assert report.survived_asteroid == 2
    assert report.survived_shots == 1
    assert report.sprites_on_screen[0] == 6
