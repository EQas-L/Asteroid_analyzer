"""Точка входа: разбор аргументов, запуск конвейера, вывод отчёта."""

import argparse
import logging
import sys
from pathlib import Path

from .errors import FatalLogError
from .metrics import MetricsCollector
from .reader import SnapshotReader
from .report import render


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="asteroid-analyzer",
        description="Анализ логов состояния Asteroid-Game",
    )
    parser.add_argument("log", type=Path, help="путь к файлу game_state.jsonl")
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="показывать предупреждения о пропущенных записях",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    logging.basicConfig(
        level=logging.WARNING if args.verbose else logging.ERROR,
        format="%(levelname)s %(name)s: %(message)s",
        stream=sys.stderr,
    )

    
    collector = MetricsCollector()
    with SnapshotReader(args.log) as reader: 
        try:
            for snapshot in reader:
                collector.update(snapshot)
        except FatalLogError as e:
            print(f"Чтение прервано: {e}", file=sys.stderr)
            sys.exit(1)

        print(render(reader.stats, collector.report()))


if __name__ == "__main__":
    main()