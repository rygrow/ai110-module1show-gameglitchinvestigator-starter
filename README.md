# Game Glitch Investigator: Number Guesser

A repaired Streamlit guessing game for the CodePath AI110 debugging assignment. Choose a difficulty and guess an integer before the attempt limit. Hints guide the next guess, and New Game starts a clean round.

## Setup

Use Python 3.10 or newer (verified here with Python 3.13).

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

On the computer used for this project, the working environment is `.venv313`:

```bash
source .venv313/bin/activate
python -m streamlit run app.py
```

## Rules

- Easy: 1–20, six attempts. Normal: 1–100, eight attempts. Hard: 1–200, five attempts.
- A valid wrong guess costs five points.
- A correct guess earns `max(10, 100 - 10 * attempt_number)` points.
- Invalid or out-of-range input consumes no attempts and changes no score.
- A correct final allowed guess wins; otherwise reaching the limit ends the round.
- Changing difficulty or pressing New Game resets score, attempts, history, feedback, and status.

Hard's 1–200 range and the consistent scoring rule are explicit design decisions; the assignment does not specify exact replacement values.

## Document Your Experience

The investigation found reversed hint text, string-based comparisons, truncated decimal input, inconsistent scoring, incorrect attempt counting, and incomplete restart state. `bug_reproduction.txt` records original behavior before repairs, including a correction to an initial assumption. Core rules now live in `logic_utils.py`, with input handling and session updates in `app.py`. The original outcome-string test contract is preserved, and new regression tests cover both rules and the Streamlit interface.

Codex implemented and tested the changes. The student chose the simpler function design over a proposed class refactor; `reflection.md` documents that real decision and clearly identifies this as an AI-assisted draft.

## Demo Walkthrough

This deterministic example is verified by `test_hints_score_and_stable_secret`; an ordinary game chooses a random secret.

1. Start Normal mode with secret 50 in the automated test: score 0 and eight attempts remain.
2. Enter 40: the game says “Go HIGHER!”, score becomes -5, and seven attempts remain.
3. Enter 70: the game says “Go LOWER!”, score becomes -10, and six attempts remain.
4. Enter 50: the game wins on attempt three, adds 70 points, and shows a final score of 60. Submission is disabled.
5. Press New Game: the game is playable again with score 0, eight attempts, empty history, and a new secret in range.
6. Enter `50.9`, `-1`, or a very large number: an error appears and no attempt is used.

## Test Results

Run `python -m pytest -q`. The three starter tests remain, with additional cases for inputs, ranges, scoring, hints, reruns, attempt limits, and restarts.

```text
...............................                                          [100%]
31 passed in 1.22s
```

The first run had a test startup timeout; the final run above uses a 15-second AppTest allowance. Automated AppTest verification exercises the Streamlit script; manual browser play is not claimed.

## Stretch Features

Challenge 1 (Advanced Edge-Case Testing) is complete. Negative numbers, decimals, and extremely large values are tested in `tests/test_app.py`, with parsing cases in `tests/test_game_logic.py`. See `ai_interactions.md` for the actual conversation, test-generation scope, and why each edge case was chosen.

## Submission

The repository includes README, reflection, AI interaction notes, automated tests, and saved test results. Progress is recorded in separate investigation, repair, and documentation commits. Review the AI-assisted reflection so it accurately represents your own understanding before submitting the public GitHub repository URL.
