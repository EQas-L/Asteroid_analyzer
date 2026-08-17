import json
from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise
from pathlib import Path
from typing import Any

import pytest

from asteroid_analyzer.errors import UnsupportedVersionError
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

UNSUPPORTEDVERSION = json.dumps({
    "v": 7,
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
    "bad_line, expected_snapshots, expected_stats, expectation",
    [
        (BROKEN_JSON,  0, ReadStats(lines_total=1, malformed_json=1), does_not_raise()),
        (UNKNOWN_TYPE, 1, ReadStats(lines_total=1, unknown_sprite_types=1, snapshots_ok=1), does_not_raise()),
        (NO_POS,       0, ReadStats(lines_total=1, incomplete_snapshots=1), does_not_raise()),
        (NO_VERSION,   0, ReadStats(lines_total=1, incomplete_snapshots=1), does_not_raise()),
        (UNSUPPORTEDVERSION, 0, ReadStats(), pytest.raises(UnsupportedVersionError))

    ],
    ids=["битый json", "неизвестный тип", "нет pos", "нет версии", "неподдерживаемая версия"],
)


def test_recoverable_errors(
    tmp_path: Path,
    bad_line: str, 
    expected_snapshots: int, 
    expected_stats: ReadStats, 
    expectation: AbstractContextManager[Any]) -> None:
    log = tmp_path / "log.jsonl"
    log.write_text(bad_line + "\n", encoding="utf-8")

    with expectation, SnapshotReader(log) as reader:
        snapshots = list(reader)

    
        assert len(snapshots) == expected_snapshots
        assert reader.stats == expected_stats
    
