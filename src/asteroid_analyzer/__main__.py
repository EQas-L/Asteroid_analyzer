from pathlib import Path

from metrics import MetricsCollector
from reader import SnapshotReader
from report import render

reader = SnapshotReader(Path("data/game_state.json"))
collector = MetricsCollector()
for snapshot in reader:
    collector.update(snapshot)
print(render(reader.stats, collector.report()))
