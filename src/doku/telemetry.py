# AI - TELEMETRY CODE BY AI
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path


@dataclass
class TechniqueStats:
    name: str
    attempts: int = 0
    successes: int = 0


@dataclass
class SolveTelemetry:
    puzzle_path: str
    started_at: str
    solved: bool = False
    elapsed_seconds: float = 0.0
    backtrack_attempts: int = 0
    max_stack_size: int = 0
    given_count: int = 0
    technique_stats: dict[str, TechniqueStats] = field(default_factory=dict)

    def record_technique(self, name: str, changed: bool) -> None:
        stats = self.technique_stats.setdefault(name, TechniqueStats(name))
        stats.attempts += 1
        if changed:
            stats.successes += 1

    def to_json(self) -> str:
        return json.dumps(asdict(self))


def new_telemetry(puzzle_path: str) -> SolveTelemetry:
    return SolveTelemetry(
        puzzle_path=puzzle_path,
        started_at=datetime.now(UTC).isoformat(),
    )


def append_to_log(telemetry: SolveTelemetry, log_path: Path) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a") as f:
        f.write(telemetry.to_json() + "\n")


def load_history(log_path: Path, puzzle_path: str) -> list[SolveTelemetry]:
    if not log_path.exists():
        return []
    records = []
    for line in log_path.read_text().splitlines():
        data = json.loads(line)
        if data["puzzle_path"] == puzzle_path:
            data["technique_stats"] = {name: TechniqueStats(**stats) for name, stats in data["technique_stats"].items()}
            records.append(SolveTelemetry(**data))
    return records
