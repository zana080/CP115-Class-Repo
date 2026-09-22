import pytest
import subprocess
import sys
import os


@pytest.fixture
def exercise_path():
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'exercise1.py')


def run_exercise(exercise_path, inputs):
    if not os.path.isfile(exercise_path):
        pytest.fail("exercise1.py was not found in the exercise1 folder")

    process = subprocess.Popen(
        [sys.executable, exercise_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    stdout, stderr = process.communicate(input=inputs)

    if process.returncode != 0:
        error = stderr.strip().splitlines()[-1] if stderr.strip() else "the program crashed"
        pytest.fail(f"the program did not run: {error}")

    return stdout


def read_lines(output, count, context):
    lines = output.replace("\r\n", "\n").strip().split('\n') if output.strip() else []
    if len(lines) != count:
        pytest.fail(
            f"{context}: expected {count} line(s) of output but got {len(lines)}. "
            f"Actual output: {output!r}"
        )
    return lines


def score_accumulator(scores):
    total = 0.0
    for s in scores:
        if s > 100:
            total += s + s * 0.20
        else:
            total += s
    return total, len(scores)


CASES = [
    [80, 120],
    [50, 50, 50],
    [100, 100],
    [200],
    [10, 20, 30, 40],
    [101, 99],
    [150, 150, 150],
    [0, 0, 0],
    [90, 110, 95, 105],
    [60],
]


@pytest.mark.parametrize("scores", CASES)
def test_score_accumulator(exercise_path, scores):
    context = f"input rounds={len(scores)}, scores={scores}"
    inputs = f"{len(scores)}\n" + "".join(f"{s}\n" for s in scores)
    output = run_exercise(exercise_path, inputs)
    line1, line2 = read_lines(output, 2, context)

    exp_total, exp_rounds = score_accumulator(scores)

    assert round(float(line1), 1) == round(exp_total, 1), f"{context} -> final score expected {round(exp_total, 1)} but got {line1!r}"
    assert line2 == str(exp_rounds), f"{context} -> rounds played expected {exp_rounds} but got {line2!r}"
