import json
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

import errors
from models import Size, Snapshot, Sprite, SpriteType, Vec2


def read_lines(path: Path) -> Iterator[tuple[str, int]]:
    """Непустые строки файла вместе с их номерами."""
    with open(path) as f:
        for lineno, line in enumerate(f, start=1):
            line = line.strip()
            if line:
                yield line, lineno


@dataclass(slots=True)
class ReadStats:
    lines_total: int = 0
    snapshots_ok: int = 0
    malformed_json: int = 0
    incomplete_snapshots: int = 0
    unknown_sprite_types: int = 0


class SnapshotReader:
    def __init__(self, path: Path, supported_version: int = 2) -> None:
        self.path = path
        self.supported_version = supported_version
        self.stats = ReadStats()

    def _parse_sprite(self, raw: dict, lineno: int) -> Sprite | None:
        """Один спрайт. None — если тип неизвестен или не нужен."""
        try:
            sprite_type = SpriteType(raw["type"])
        except ValueError:
            raise errors.UnknownSpriteTypeError(lineno, raw.get("type")) from None

        if sprite_type is SpriteType.ASTEROID_FIELD:
            return None

        return Sprite(
            id=raw["id"],
            type=sprite_type,
            position=Vec2(raw["pos"][0], raw["pos"][1]),
            velocity=Vec2(raw["vel"][0], raw["vel"][1]),
            radius=raw["rad"],
            rotation=raw.get("rot"),
        )

    def _parse_snapshot(self, line: str, lineno: int) -> Snapshot:
        try:
            record = json.loads(line)
        except json.JSONDecodeError as e:
            raise errors.MalformedLineError(lineno, str(e)) from e

        try:
            if record["v"] != self.supported_version:
                raise errors.UnsupportedVersionError(
                    lineno, record["v"], self.supported_version
                )

            sprites: list[Sprite] = []
            for raw in record["updatable"]["sprites"]:
                try:
                    sprite = self._parse_sprite(raw, lineno)
                except errors.UnknownSpriteTypeError as e:
                    print(f"предупреждение: {e}")
                    self.stats.unknown_sprite_types += 1
                    continue
                if sprite is not None:
                    sprites.append(sprite)

            return Snapshot(
                v=record["v"],
                timestamp=record["timestamp"],
                elapsed_s=record["elapsed_s"],
                frame=record["frame"],
                screen=Size(width = record["screen_size"][0], height =record["screen_size"][1]),
                sprites=tuple(sprites),
            )
        except KeyError as e:
            raise errors.IncompleteRecordError(lineno, e.args[0]) from e

    def __iter__(self) -> Iterator[Snapshot]:
        for line, lineno in read_lines(self.path):
            self.stats.lines_total += 1
            try:
                snapshot = self._parse_snapshot(line, lineno)
            except errors.MalformedLineError as e:
                print(f"пропуск: {e}")
                self.stats.malformed_json += 1
                continue
            except errors.IncompleteRecordError as e:
                print(f"пропуск: {e}")
                self.stats.incomplete_snapshots += 1
                continue
            self.stats.snapshots_ok += 1
            yield snapshot