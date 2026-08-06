import reader
from pathlib import Path

if __name__ == "__main__":
    snaps = list(reader.read_snapshots(Path("data/game_state.json")))
    print("снимков:", len(snaps))
    print("спрайтов в первом:", len(snaps[0].sprites))
    print(snaps[0].sprites[0])
print("сумма спрайтов:", sum(len(s.sprites) for s in snaps))