"""Pure, independently testable rules for the guessing game."""


def get_range_for_difficulty(difficulty: str):
    """Return inclusive bounds; unknown difficulties use Normal bounds."""
    return {"Easy": (1, 20), "Normal": (1, 100), "Hard": (1, 200)}.get(
        difficulty, (1, 100)
    )


def parse_guess(raw: str):
    """Accept integer text; return (success, value, error)."""
    if raw is None or not raw.strip():
        return False, None, "Enter a guess."
    # FIX: AI-assisted validation rejects decimals instead of truncating them.
    try:
        return True, int(raw.strip()), None
    except ValueError:
        return False, None, "Enter a whole number."


def check_guess(guess: int, secret: int):
    """Return an outcome string for two integer values."""
    # FIX: Keep numeric comparisons here and presentation in app.py.
    if guess == secret:
        return "Win"
    return "Too High" if guess > secret else "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Deduct five for misses; award max(10, 100-10*attempt) on a win."""
    # FIX: One-based attempts give 90 points for a first-guess win.
    if outcome == "Win":
        return current_score + max(10, 100 - 10 * attempt_number)
    if outcome in ("Too High", "Too Low"):
        return current_score - 5
    return current_score
