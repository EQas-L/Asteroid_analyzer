import json
import logging
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any, TextIO

from .errors import (
    IncompleteRecordError,
    MalformedLineError,
    UnknownSpriteTypeError,
    UnsupportedVersionError,
)
from .models import Size, Snapshot, Sprite, SpriteType, Vec2

logger = logging.getLogger(__name__)


class Vex:
    x = 1


def read_lines(f: TextIO) -> Iterator[tuple[str, int]]:
    """Непустые строки файла вместе с их номерами."""
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
        self._file: TextIO | None

    def __enter__(self) -> "SnapshotReader":
        self._file = self.path.open()
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        if self._file is not None:
            self._file.close()
            self._file = None

    def _parse_sprite(self, raw: dict, lineno: int) -> Sprite | None:
        """Один спрайт. None — если тип неизвестен или не нужен."""
        try:
            sprite_type = SpriteType(raw["type"])
        except ValueError:
            raise UnknownSpriteTypeError(lineno, raw.get("type")) from None

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
            raise MalformedLineError(lineno, str(e)) from e

        try:
            if record["v"] != self.supported_version:
                raise UnsupportedVersionError(lineno, record["v"], self.supported_version)

            sprites: list[Sprite] = []
            for raw in record["updatable"]["sprites"]:
                try:
                    sprite = self._parse_sprite(raw, lineno)
                except UnknownSpriteTypeError as e:
                    logger.warning("предупреждение: %s", e)
                    self.stats.unknown_sprite_types += 1
                    continue
                if sprite is not None:
                    sprites.append(sprite)

            return Snapshot(
                v=record["v"],
                timestamp=record["timestamp"],
                elapsed_s=record["elapsed_s"],
                frame=record["frame"],
                screen=Size(width=record["screen_size"][0], height=record["screen_size"][1]),
                sprites=tuple(sprites),
            )
        except KeyError as e:
            raise IncompleteRecordError(lineno, e.args[0]) from e

    def __iter__(self) -> Iterator[Snapshot]:
        f = self._file
        if f is None:
            raise RuntimeError("...")
        for line, lineno in read_lines(f):
            self.stats.lines_total += 1
            try:
                snapshot = self._parse_snapshot(line, lineno)
            except MalformedLineError as e:
                logger.warning("пропуск: %s", e)
                self.stats.malformed_json += 1
                continue
            except IncompleteRecordError as e:
                logger.warning("пропуск: %s", e)
                self.stats.incomplete_snapshots += 1
                continue
            self.stats.snapshots_ok += 1
            yield snapshot
