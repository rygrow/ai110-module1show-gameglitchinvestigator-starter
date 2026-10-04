import pytest

from logic_utils import (
    check_guess, get_range_for_difficulty, parse_guess, update_score,
)


def test_winning_guess():
    assert check_guess(50, 50) == "Win"


def test_guess_too_high():
    assert check_guess(60, 50) == "Too High"


def test_guess_too_low():
    assert check_guess(40, 50) == "Too Low"


@pytest.mark.parametrize("raw", ["", "   ", None, "abc", "50.9", "1e2", "inf"])
def test_invalid_input(raw):
    ok, value, error = parse_guess(raw)
    assert not ok and value is None and error


@pytest.mark.parametrize("raw,value", [(" 50 ", 50), ("-1", -1), ("0", 0), ("999999999999999999999", 999999999999999999999)])
def test_integer_parsing(raw, value):
    assert parse_guess(raw) == (True, value, None)


@pytest.mark.parametrize("difficulty,bounds", [("Easy", (1, 20)), ("Normal", (1, 100)), ("Hard", (1, 200)), ("unknown", (1, 100))])
def test_difficulty(difficulty, bounds):
    assert get_range_for_difficulty(difficulty) == bounds


@pytest.mark.parametrize("outcome", ["Too High", "Too Low"])
@pytest.mark.parametrize("attempt", [1, 2, 3])
def test_misses_always_cost_five(outcome, attempt):
    assert update_score(0, outcome, attempt) == -5


def test_first_guess_win():
    assert update_score(0, "Win", 1) == 90


def test_win_reward_floor():
    assert update_score(-45, "Win", 10) == -35
