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


def grocery(p1, q1, p2, q2, p3, q3):
    subtotal = p1 * q1 + p2 * q2 + p3 * q3
    tax = subtotal * 0.06
    total = subtotal + tax
    return subtotal, tax, total


CASES = [
    (4.50, 3, 2.80, 2, 0.60, 6),
    (10.00, 1, 5.00, 2, 2.50, 4),
    (1.20, 10, 0.00, 0, 3.30, 3),
    (99.99, 2, 15.50, 1, 7.25, 8),
    (0.00, 0, 0.00, 0, 0.00, 0),
]


@pytest.mark.parametrize("p1,q1,p2,q2,p3,q3", CASES)
def test_grocery(exercise_path, p1, q1, p2, q2, p3, q3):
    context = f"input {p1},{q1},{p2},{q2},{p3},{q3}"
    inputs = f"{p1}\n{q1}\n{p2}\n{q2}\n{p3}\n{q3}\n"
    output = run_exercise(exercise_path, inputs)
    subtotal, tax, total = read_numbers(output, 3, context)

    exp_subtotal, exp_tax, exp_total = grocery(p1, q1, p2, q2, p3, q3)

    assert round(subtotal, 2) == round(exp_subtotal, 2), f"{context} -> subtotal expected {round(exp_subtotal, 2)} but got {round(subtotal, 2)}"
    assert round(tax, 2) == round(exp_tax, 2), f"{context} -> tax expected {round(exp_tax, 2)} but got {round(tax, 2)}"
    assert round(total, 2) == round(exp_total, 2), f"{context} -> total expected {round(exp_total, 2)} but got {round(total, 2)}"
