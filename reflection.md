# Reflection: Game Glitch Investigator

Process note: Codex performed the initial code investigation, implementation, and automated verification. The student requested help completing the assignment and explicitly chose the simpler function approach over the proposed Game class. This reflection is an AI-assisted draft grounded in that exchange and the recorded test evidence; it does not claim the student manually performed those steps.

## 1. What was broken when you started?

The original functions were executed in isolation before editing, and the UI code was inspected; the original game was not manually played in a browser. A guess of 60 against 50 produced a “Too High” outcome but told the player to go higher. The app sometimes converted the secret to a string, which caused the fallback to compare numbers lexicographically. Decimal inputs were silently truncated, attempts started at one, and New Game did not reset status, score, or history.

**Bug Reproduction Log**

| Input / trigger | Expected behavior | Actual original behavior | Evidence |
|---|---|---|---|
| `check_guess(60, 50)` | Too High; go lower | Too High; “Go HIGHER!” | Original function execution in `bug_reproduction.txt` |
| `check_guess(9, "50")` | Numeric comparison says Too Low | String fallback says Too High | Original fallback compares `"9" > "50"` |
| `parse_guess("50.9")` | Reject non-integer text | Accepts integer 50 | Original function execution |
| `update_score(0, "Too High", 2)` | Consistent miss penalty of -5 | Score increases to 5 | Original function execution |
| Blank submission | Error without using an attempt | Attempts increment before validation | Original UI code inspection |
| New Game after winning | Fresh playable round | Status remains won; score/history remain | Original reset block inspection |

The initial reproduction note incorrectly described the equal mixed-type case as a failed win. Actual execution showed `check_guess(50, "50")` still wins; the note was corrected in the second commit. This correction distinguishes measured behavior from an initial assumption.

## 2. How did you use AI as a teammate?

Codex suggested extracting pure functions into `logic_utils.py` and keeping both operands as integers, which correctly removes the misleading string comparison and makes the original three tests pass. Its accepted fixes were verified with pytest and Streamlit AppTest rather than trusting the explanation alone. Codex also proposed a Game class for centralized state management, and I asked whether the assignment required that approach. After learning it did not, I explicitly chose simple functions and session state because a class would add complexity without helping this small assignment. The function version passed the same win, loss, difficulty-change, and restart checks, showing that the simpler design met the requirements.

## 3. Debugging and testing your fixes

Codex generated regression tests for numeric comparisons, decimal rejection, scoring, and invalid input. Streamlit AppTest additionally exercised the actual UI callbacks, checking that guesses of 40, 70, and 50 produce the right hints and a final score of 60. Tests also verify the exact attempt limit, winning on the final allowed attempt, and restarting after both a win and a loss. The first test run had 30 passes and one startup timeout, so the test startup allowance was increased from three to fifteen seconds; the final run passed all 31 tests. Negative numbers, decimal text, and extremely large integers are covered, and `test_results.txt` records the actual final output.

## 4. What did you learn about Streamlit and state?

Streamlit runs the script again when a user interacts with a widget. Ordinary variables are recreated, while session state preserves values for that user's session. The starter already preserved the secret number, so the README's claim that it necessarily changed on every submission was not supported by the code. Callback functions now update the state before the page is redrawn, keeping the displayed score and remaining attempts current. New Game and difficulty changes initialize every round field together.

## 5. Looking ahead: your developer habits

A useful habit to carry forward is to reproduce a bug with a small concrete example before accepting an AI repair. Next time, I would spend more time playing the original game myself and reviewing each diff before moving to the next phase. This project shows that AI-generated code and even AI explanations can include incorrect assumptions or a contract mismatch. Human-in-the-loop decisions, a focused test set, and verification help detect that kind of hallucination rather than treating generated code as automatically correct.
