import pytest
import subprocess
import sys
import os


@pytest.fixture
def exercise_path():
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'exercise3.py')


def run_exercise(exercise_path, inputs):
    if not os.path.isfile(exercise_path):
        pytest.fail("exercise3.py was not found in the exercise3 folder")

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


def point_accumulator(target, points):
    # Mirrors the loop: add points until total reaches or passes the target.
    total = 0
    rounds = 0
    for p in points:
        if total >= target:
            break
        total += p
        rounds += 1
    return total, rounds


CASES = [
    (100, [30, 45, 35]),
    (50, [50]),
    (60, [20, 20, 20]),
    (100, [100]),
    (200, [70, 70, 70]),
    (10, [3, 3, 3, 3]),
    (75, [25, 25, 25]),
    (150, [40, 40, 40, 40]),
    (90, [90]),
    (120, [50, 50, 50]),
]


@pytest.mark.parametrize("target,points", CASES)
def test_point_accumulator(exercise_path, target, points):
    context = f"input target={target}, points entered={points}"
    inputs = f"{target}\n" + "".join(f"{p}\n" for p in points)
    output = run_exercise(exercise_path, inputs)
    line1, line2 = read_lines(output, 2, context)

    exp_total, exp_rounds = point_accumulator(target, points)

    assert line1 == str(exp_total), f"{context} -> final total expected {exp_total} but got {line1!r}"
    assert line2 == str(exp_rounds), f"{context} -> rounds played expected {exp_rounds} but got {line2!r}"
