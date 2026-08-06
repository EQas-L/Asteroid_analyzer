from pathlib import Path
import errors
from reader import SnapshotReader

reader = SnapshotReader(Path("data/game_state.json"))
try:
    for snap in reader:
        print(f"ok: кадр {snap.frame}, спрайтов {len(snap.sprites)}")
except errors.FatalLogError as e:
    print(f"ОСТАНОВКА: {e}")
print()
print(reader.stats)