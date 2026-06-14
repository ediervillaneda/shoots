import json
from pathlib import Path

_SCORES_PATH = Path.home() / ".starfall" / "scores.json"
_MAX_ENTRIES = 10


def load() -> list[dict]:
    if not _SCORES_PATH.exists():
        return []
    try:
        return json.loads(_SCORES_PATH.read_text())
    except (json.JSONDecodeError, OSError):
        return []


def save(initials: str, score: int, current: list[dict]) -> list[dict]:
    current.append({"initials": initials[:3].upper(), "score": score})
    current.sort(key=lambda x: x["score"], reverse=True)
    current = current[:_MAX_ENTRIES]
    _SCORES_PATH.parent.mkdir(parents=True, exist_ok=True)
    _SCORES_PATH.write_text(json.dumps(current, indent=2))
    return current


def qualifies(score: int, current: list[dict]) -> bool:
    if len(current) < _MAX_ENTRIES:
        return True
    return score > current[-1]["score"]
