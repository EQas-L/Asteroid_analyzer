from asteroid_analyzer.metrics import ObjectLife, Report
from asteroid_analyzer.models import SpriteType
from asteroid_analyzer.reader import ReadStats
from asteroid_analyzer.report import render

# Объект со статистикой чтения/парсинга данных
test_read_stats = ReadStats(
    lines_total=1000,
    snapshots_ok=965,
    malformed_json=15,
    incomplete_snapshots=12,
    unknown_sprite_types=8,
)

# Объект итогового отчета с согласованными типами и значениями
test_report = Report(
    asteroid_area_fraction=[0.05, 0.08, 0.12, 0.07, 0.03],
    sprites_on_screen=[4, 6, 9, 7, 3],
    sprites_appearance_by_type={
        SpriteType.PLAYER: 1,
        SpriteType.ASTEROID: 15,
        SpriteType.SHOT: 30,
        SpriteType.ASTEROID_FIELD: 1,
    },
    asteroids_destroyed=12,
    shots_hit_fraction=0.40,  # 12 попаданий из 30 выстрелов
    objects_life_time={
        1: (300, SpriteType.PLAYER),
        2: (45, SpriteType.ASTEROID),
        3: (12, SpriteType.SHOT),
        4: (80, SpriteType.ASTEROID),
    },
    survived_asteroid=3,  # 15 появилось - 12 уничтожено = 3 уцелело
    survived_shots=0,
    objects_life={
        1: ObjectLife(
            id=1,
            sprite_type=SpriteType.PLAYER,
            first_frame=0,
            last_frame=300,
        ),
        2: ObjectLife(
            id=2,
            sprite_type=SpriteType.ASTEROID,
            first_frame=10,
            last_frame=55,
        ),
        3: ObjectLife(
            id=3,
            sprite_type=SpriteType.SHOT,
            first_frame=40,
            last_frame=52,
        ),
        4: ObjectLife(
            id=4,
            sprite_type=SpriteType.ASTEROID,
            first_frame=50,
            last_frame=130,
        ),
    },
)

def test_render() -> None:
    text = render(test_read_stats, test_report).splitlines()
    required_line = [line for line in text if 'астероид' in line and 'живы' in line][0].split()
    ind = [i for i in range(len(required_line)) if ')' in required_line[i]][0]
    survived_asteroid = int(required_line[ind+1])
    assert survived_asteroid == test_report.survived_asteroid

