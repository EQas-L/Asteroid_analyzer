import json

import pytest
from asteroid_analyzer.reader import ReadStats, SnapshotReader

BROKEN_JSON = '{"v": 2, "timestamp": "18:00:02.000", "frame": 120'
UNKNOWN_TYPE = json.dumps({
    "v": 2, 
    "timestamp": "11:35:52.480", 
    "elapsed_s": 1, 
    "frame": 60, 
    "screen_size": [1280, 720], 
    "updatable": {
        "count": 3, 
        "sprites": [{
            "type": "Alien", 
            "id": 1, 
            "pos": [652.68, 361.27], 
            "vel": [0.0, 0.0], 
            "rad": 20, 
            "rot": -91.5
            }]
        }
    })

NO_POS = json.dumps({
    "v": 2, 
    "timestamp": "11:35:52.480", 
    "elapsed_s": 1, 
    "frame": 60, 
    "screen_size": [1280, 720], 
    "updatable": {
        "count": 3, 
        "sprites": [{
            "type": "Player", 
            "id": 1,
            "vel": [0.0, 0.0], 
            "rad": 20, 
            "rot": -91.5
            }]
        }
    })
NO_VERSION = json.dumps({
    "timestamp": "11:35:52.480", 
    "elapsed_s": 1, 
    "frame": 60, 
    "screen_size": [1280, 720], 
    "updatable": {
        "count": 3, 
        "sprites": [{
            "type": "Shot", 
            "id": 1, 
            "pos": [652.68, 361.27], 
            "vel": [0.0, 0.0], 
            "rad": 20, 
            "rot": -91.5
            }]
        }
    })


@pytest.mark.parametrize(
    "bad_line, expected_snapshots, expected_stats",
    [
        (BROKEN_JSON,  0, ReadStats(lines_total=1, malformed_json=1)),
        (UNKNOWN_TYPE, 1, ReadStats(lines_total=1, unknown_sprite_types=1, snapshots_ok=1)),
        (NO_POS,       0, ReadStats(lines_total=1, incomplete_snapshots=1)),
        (NO_VERSION,   0, ReadStats(lines_total=1, incomplete_snapshots=1))
    ],
    ids=["битый json", "неизвестный тип", "нет pos", "нет версии"],
)
def test_recoverable_errors(tmp_path, bad_line, expected_snapshots, expected_stats):
    log = tmp_path / "log.jsonl"
    log.write_text(bad_line + "\n", encoding="utf-8")

    with SnapshotReader(log) as reader:
        snapshots = list(reader)

    assert len(snapshots) == expected_snapshots
    assert reader.stats == expected_stats