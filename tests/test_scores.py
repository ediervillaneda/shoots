import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path


def test_load_returns_empty_when_no_file(tmp_path):
    import src.systems.scores as scores
    with patch.object(type(scores._SCORES_PATH), 'exists', lambda self: False):
        result = scores.load()
    assert result == []


def test_load_returns_empty_on_corrupt_json(tmp_path):
    import src.systems.scores as scores
    fake_path = tmp_path / "scores.json"
    fake_path.write_text("not valid json")
    with patch('src.systems.scores._SCORES_PATH', fake_path):
        result = scores.load()
    assert result == []


def test_save_returns_sorted_descending(tmp_path):
    import src.systems.scores as scores
    with patch('src.systems.scores._SCORES_PATH', tmp_path / "scores.json"):
        result = scores.save("AAA", 100, [{"initials": "BBB", "score": 200}])
    assert result[0]["score"] == 200
    assert result[1]["score"] == 100


def test_save_does_not_exceed_max_entries(tmp_path):
    import src.systems.scores as scores
    current = [{"initials": "XX", "score": i * 10} for i in range(10)]
    with patch('src.systems.scores._SCORES_PATH', tmp_path / "scores.json"):
        result = scores.save("NEW", 999, current)
    assert len(result) <= 10


def test_qualifies_true_when_list_empty():
    import src.systems.scores as scores
    assert scores.qualifies(1, []) is True


def test_qualifies_true_when_list_less_than_max():
    import src.systems.scores as scores
    assert scores.qualifies(1, [{"initials": "A", "score": 999}]) is True


def test_qualifies_true_when_score_beats_minimum():
    import src.systems.scores as scores
    current = [{"initials": "X", "score": i * 10} for i in range(10, 0, -1)]
    assert scores.qualifies(10000, current) is True


def test_qualifies_false_when_score_too_low():
    import src.systems.scores as scores
    current = [{"initials": "X", "score": i * 100} for i in range(10, 0, -1)]
    assert scores.qualifies(1, current) is False
