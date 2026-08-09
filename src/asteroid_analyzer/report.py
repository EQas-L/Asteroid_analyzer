from .metrics import Report
from .reader import ReadStats


def render(read_stats: ReadStats, report: Report) -> str:
    return f"""
Общее количество строк: {read_stats.lines_total}
Неразобранных строк по причине неправильного формата: {read_stats.malformed_json}
Количество успешно обработанных снимков: {read_stats.snapshots_ok}
Неразобранных снимков по причине неправильного формата строки: {read_stats.incomplete_snapshots}
Неизвестных типов спрайтов: {read_stats.unknown_sprite_types}
создано всего: {max(report.objects_life)}
наблюдалось  : {len(report.objects_life)}
объектов на экране (среднее, максимум): {report.average_sprites, report.max_sprites}
доля площади астероидов (средняя, максимальная): { report.average_fraction, report.max_fraction}
разрушено астероидов: {report.asteroids_destroyed}
точность стрельбы% (нижняя оценка): {report.shots_hit_fraction * 100:.0f} %
время жизни астероидов: {report.average_life_time_asteroids}, живы в конце(не вошли в учет): {report.survived_asteroid}
время жизни снарядов: {report.average_life_time_shots}, живы в конце(не вошли в учет): {report.survived_shots}
"""