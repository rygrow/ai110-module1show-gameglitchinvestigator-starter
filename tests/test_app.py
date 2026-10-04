"""Exercise Streamlit callbacks, reruns, and the visible game."""
from pathlib import Path

from streamlit.testing.v1 import AppTest

APP = Path(__file__).resolve().parents[1] / "app.py"


def game(secret=50):
    app = AppTest.from_file(str(APP), default_timeout=15).run()
    app.session_state.secret = secret
    return app


def guess(app, value):
    app.text_input[0].set_value(value)
    app.button[0].click().run()
    assert not app.exception
    return app


def test_hints_score_and_stable_secret():
    app = game()
    guess(app, "40")
    assert "HIGHER" in app.warning[0].value
    assert app.session_state.secret == 50
    assert app.session_state.attempts == 1
    guess(app, "70")
    assert "LOWER" in app.warning[0].value
    assert app.session_state.score == -10
    guess(app, "50")
    assert app.session_state.status == "won"
    assert app.session_state.score == 60
    assert app.button[0].disabled


def test_invalid_and_out_of_range_do_not_consume_attempts():
    app = game()
    for value in ["", "abc", "50.9", "-1", "0", "999999999999999999999"]:
        guess(app, value)
        assert app.error
        assert app.session_state.attempts == 0
        assert app.session_state.score == 0
        assert app.session_state.history == []


def test_loss_at_exact_limit_and_restart():
    app = game()
    for _ in range(8):
        guess(app, "1")
    assert app.session_state.status == "lost"
    assert "Attempts left: 0" in app.info[0].value
    app.button[1].click().run()
    assert not app.exception
    assert app.session_state.status == "playing"
    assert app.session_state.attempts == 0
    assert app.session_state.score == 0
    assert app.session_state.history == []
    assert app.text_input[0].value == ""


def test_difficulty_resets_round_in_selected_range():
    app = game()
    guess(app, "40")
    app.selectbox[0].select("Easy").run()
    assert not app.exception
    assert 1 <= app.session_state.secret <= 20
    assert app.session_state.attempts == 0
    assert "between 1 and 20" in app.info[0].value
    app.button[1].click().run()
    assert 1 <= app.session_state.secret <= 20


def test_last_attempt_can_win_and_restart_after_win():
    app = game()
    for _ in range(7):
        guess(app, "1")
    guess(app, "50")
    assert app.session_state.status == "won"
    app.button[1].click().run()
    assert app.session_state.status == "playing"
    assert not app.button[0].disabled
