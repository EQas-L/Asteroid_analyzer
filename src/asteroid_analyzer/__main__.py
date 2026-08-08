from pathlib import Path

import errors
from metrics import MetricsCollector
from reader import SnapshotReader

reader = SnapshotReader(Path("data/game_state.json"))


collector = MetricsCollector()
for snapshot in SnapshotReader(Path("data/game_state.json")):
    collector.update(snapshot)
r = collector.report()
print("на экране:", r.sprites_on_screen)
print("доля     :", [round(x, 3) for x in r.asteroid_area_fraction])
print("по типам :", r.sprites_appearance_by_type)
print("разрушено астероидов:", r.asteroids_destroyed)
print("попаданий в астероиды:", round(r.percent_shots_hit *100, 1), "%")
print(f'Дожило до конца: {len(r.survived)} объектов')
print("создано всего:", max(collector.objects_life))     # максимальный id
print("наблюдалось  :", len(collector.objects_life))