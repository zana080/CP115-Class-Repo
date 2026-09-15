import pytest
import subprocess
import sys
import os


@pytest.fixture
def exercise_path():
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'exercise4.py')


def run_exercise(exercise_path, inputs):
    if not os.path.isfile(exercise_path):
        pytest.fail("exercise4.py was not found in the exercise4 folder")

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


def read_numbers(output, count, context):
    lines = output.strip().split('\n') if output.strip() else []
    if len(lines) != count:
        pytest.fail(
            f"{context}: expected {count} line(s) of output but got {len(lines)}. "
            f"Actual output: {output!r}"
        )
    try:
        return [float(line) for line in lines]
    except ValueError:
        pytest.fail(
            f"{context}: every output line must be a plain number. "
            f"Actual output: {output!r}"
        )


def water(current, previous):
    consumption = current - previous
    if consumption <= 20:
        cost = consumption * 0.57
    elif consumption <= 35:
        cost = 20 * 0.57 + (consumption - 20) * 1.03
    else:
        cost = 20 * 0.57 + 15 * 1.03 + (consumption - 35) * 1.40
    total = cost + 8 + 2
    return consumption, cost, total


CASES = [
    (15, 0),
    (30, 0),
    (50, 0),
    (100, 30),
    (135, 100),
    (20, 0),
    (35, 0),
    (36, 0),
    (60, 10),
    (21, 0),
]


@pytest.mark.parametrize("current,previous", CASES)
def test_water(exercise_path, current, previous):
    context = f"input current={current}, previous={previous}"
    inputs = f"{current}\n{previous}\n"
    output = run_exercise(exercise_path, inputs)
    consumption, cost, total = read_numbers(output, 3, context)

    exp_consumption, exp_cost, exp_total = water(current, previous)

    assert round(consumption, 2) == round(exp_consumption, 2), f"{context} -> consumption expected {round(exp_consumption, 2)} but got {round(consumption, 2)}"
    assert round(cost, 2) == round(exp_cost, 2), f"{context} -> water_cost expected {round(exp_cost, 2)} but got {round(cost, 2)}"
    assert round(total, 2) == round(exp_total, 2), f"{context} -> total_bill expected {round(exp_total, 2)} but got {round(total, 2)}"
