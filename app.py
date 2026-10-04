"""Streamlit interface for the repaired number guessing game."""
import random

import streamlit as st

from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)


def reset_game(difficulty):
    """Initialize every round field using the selected difficulty."""
    low, high = get_range_for_difficulty(difficulty)
    # FIX: AI-assisted reset covers terminal status, history, and score.
    st.session_state.update(
        secret=random.randint(low, high), attempts=0, score=0,
        status="playing", history=[], difficulty=difficulty, feedback=None,
        guess_input="",
    )


def submit_guess():
    """Validate before consuming an attempt, then update the round once."""
    if st.session_state.status != "playing":
        return
    ok, guess, error = parse_guess(st.session_state.guess_input)
    low, high = get_range_for_difficulty(st.session_state.difficulty)
    if not ok:
        st.session_state.feedback = ("Invalid", error)
        return
    if not low <= guess <= high:
        st.session_state.feedback = (
            "Invalid", f"Enter a number between {low} and {high}."
        )
        return
    # FIX: Secret stays an integer; only valid guesses consume attempts.
    st.session_state.attempts += 1
    outcome = check_guess(guess, st.session_state.secret)
    st.session_state.history.append(guess)
    st.session_state.score = update_score(
        st.session_state.score, outcome, st.session_state.attempts
    )
    st.session_state.feedback = (outcome, {
        "Win": "🎉 Correct!", "Too High": "📉 Go LOWER!",
        "Too Low": "📈 Go HIGHER!",
    }[outcome])
    if outcome == "Win":
        st.session_state.status = "won"
    elif st.session_state.attempts >= ATTEMPT_LIMITS[st.session_state.difficulty]:
        st.session_state.status = "lost"


ATTEMPT_LIMITS = {"Easy": 6, "Normal": 8, "Hard": 5}
st.set_page_config(page_title="Number Guesser", page_icon="🎮")
st.title("🎮 Game Glitch Investigator")
st.caption("Guess the secret number before your attempts run out.")
st.sidebar.header("Settings")
difficulty = st.sidebar.selectbox("Difficulty", ["Easy", "Normal", "Hard"], index=1)
if "secret" not in st.session_state or st.session_state.difficulty != difficulty:
    reset_game(difficulty)
low, high = get_range_for_difficulty(difficulty)
attempt_limit = ATTEMPT_LIMITS[difficulty]
st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")
st.info(f"Guess a number between {low} and {high}. "
        f"Attempts left: {attempt_limit - st.session_state.attempts}")
st.metric("Score", st.session_state.score)
st.text_input("Enter your guess:", key="guess_input",
              disabled=st.session_state.status != "playing")
col1, col2, col3 = st.columns(3)
with col1:
    st.button("Submit Guess 🚀", on_click=submit_guess,
              disabled=st.session_state.status != "playing")
with col2:
    st.button("New Game 🔁", on_click=reset_game, args=(difficulty,))
with col3:
    show_hint = st.checkbox("Show hint", value=True)
if st.session_state.feedback:
    outcome, message = st.session_state.feedback
    if outcome == "Invalid":
        st.error(message)
    elif show_hint and outcome != "Win":
        st.warning(message)
if st.session_state.status == "won":
    st.success(f"You won! The secret was {st.session_state.secret}. "
               f"Final score: {st.session_state.score}")
elif st.session_state.status == "lost":
    st.error(f"Out of attempts! The secret was {st.session_state.secret}. "
             f"Score: {st.session_state.score}")
with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)
