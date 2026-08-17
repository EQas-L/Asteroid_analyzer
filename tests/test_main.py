from pathlib import Path

import pytest

from asteroid_analyzer.errors import FatalLogError
from asteroid_analyzer.metrics import MetricsCollector
from asteroid_analyzer.reader import SnapshotReader

file = Path(__file__).parent.parent / "data/broken.jsonl"




def test_main() -> None:
    collector = MetricsCollector()
    with pytest.raises(FatalLogError), SnapshotReader(file) as reader:
        for snapshot in reader:
            collector.update(snapshot)
    assert reader.stats.malformed_json == 1
    assert reader.stats.incomplete_snapshots == 2
    assert reader.stats.snapshots_ok == 3
    assert reader.stats.lines_total == 7
    rep = collector.report()
    assert max(rep.sprites_on_screen) == 2
    assert max(rep.asteroid_area_fraction) == 0.00545415391248228
    assert rep.asteroids_destroyed == 0
    assert rep.survived_asteroid == 1
    assert rep.survived_shots == 0
    assert rep.shots_hit_fraction == 0.0
    assert rep.objects_life_time == {}


