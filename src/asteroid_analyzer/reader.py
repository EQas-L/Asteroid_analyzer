import json
from collections.abc import Iterable, Iterator
from pathlib import Path

from models import Size, Snapshot, Sprite, SpriteType, Vec2


def read_lines(path: Path) -> Iterator[str]:
    """Строки файла, без пустых и без завершающего перевода строки."""
    with open(path, 'r') as f:
        for line in f:
            line  = line.strip()
            if line:
                yield line


def parse_json(lines: Iterable[str]) -> Iterator[dict]:
    """Строки → разобранные словари."""
    for line in lines:
        yield json.loads(line)


def to_snapshots(records: Iterable[dict]) -> Iterator[Snapshot]:
    """Словари → объекты Snapshot."""
    skipped = 0
    for record in records:
        sprites: list[Sprite] = []
        for sprite in record['updatable']['sprites']:
            try:
                sprite_type = SpriteType(sprite["type"])
            except ValueError:
                skipped += 1
                continue

            if sprite_type is SpriteType.ASTEROID_FIELD:
                continue
            sprites.append(Sprite(  
                id=sprite['id'],
                type=sprite_type,
                position=Vec2(sprite['pos'][0], sprite['pos'][1]),
                velocity=Vec2(sprite['vel'][0], sprite['vel'][1]),
                radius=sprite['rad'],
                rotation=sprite.get('rot')
                ))
        yield Snapshot(
            v=record['v'],
            timestamp=record['timestamp'],
            elapsed_s=record['elapsed_s'],
            frame=record['frame'],
            screen=Size(record['screen_size'][0], record['screen_size'][1]),
            sprites=tuple(sprites)
            )


        

def read_snapshots(path: Path) -> Iterator[Snapshot]:
    return to_snapshots(parse_json(read_lines(path)))
if __name__ == "__main__":
    snaps = list(read_snapshots(Path("data/game_state.json")))
    print("снимков:", len(snaps))
    print("спрайтов в первом:", len(snaps[0].sprites))
    print(snaps[0].sprites[0])