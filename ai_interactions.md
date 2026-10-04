# AI Interactions — Challenge 1: Advanced Edge-Case Testing

## Actual user requests

- “幫我完成這個作業” — Help me complete this assignment.
- “我有一個小時 可以做” — I have one hour available.
- “它有說一定要用類別集中管理狀態 嗎” — Does it require a class to manage state?
- “採用函式方案，記錄拒絕類別的理由” — Use functions and record the reason for rejecting a class.

## Test-generation instructions

No separate student prompt was entered for edge-case generation. Codex inferred testing work from the supplied assignment and generated the suite under the student's request to complete it. The following describes the test-generation scope, rather than inventing a prompt the student sent:

“Verify numeric hints and scoring; reject decimal, blank, and nonnumeric text; reject negative and extremely large guesses at the UI range boundary without consuming attempts; test win, loss, restart, and difficulty changes through Streamlit AppTest.”

- Negative numbers: valid integer syntax but outside every supported range.
- Decimal text: catches the original silent truncation bug.
- Extremely large integers: parses safely but must be rejected by the game's range validation.

## Workflow and judgment

Codex edited `app.py`, `logic_utils.py`, the two test files, requirements, and documentation. Core rules became pure functions, while UI callbacks manage session state. The student explicitly declined the more complex Game-class suggestion after confirming it was not required. No student manual code changes or browser testing are claimed.

The three original tests expect an outcome string, while the original function returned a tuple and the utility stubs raised `NotImplementedError`. The implementation preserves the tests' string contract and puts hint text in the UI. The agent corrected its initial inaccurate mixed-type reproduction note after execution showed that the equal case still wins.

## Verification

The first full run reported 30 passes and one cold-start timeout. Increasing AppTest's startup allowance to 15 seconds produced the final output saved in `test_results.txt` and copied into the README. AppTest runs the real Streamlit script and callbacks; it is not a claim of manual browser testing.
