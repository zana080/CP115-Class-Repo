import pytest
import subprocess
import sys
import os


@pytest.fixture
def exercise_path():
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'exercise6.py')


def run_exercise(exercise_path, inputs):
    if not os.path.isfile(exercise_path):
        pytest.fail("exercise6.py was not found in the exercise6 folder")

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


RATES = {"Manager": 30, "Supervisor": 20, "Staff": 15, "Intern": 8}


def overtime(position, hours, is_weekend):
    rate = RATES[position]
    if hours <= 8:
        pay = hours * rate * 1.5
    else:
        pay = 8 * rate * 1.5 + (hours - 8) * rate * 2.0
    if is_weekend == "yes":
        pay = pay + hours * 5
    return pay


CASES = [
    ("Manager", 5, "no"),
    ("Supervisor", 10, "no"),
    ("Staff", 8, "yes"),
    ("Intern", 12, "yes"),
    ("Manager", 8, "no"),
    ("Staff", 15, "no"),
    ("Supervisor", 3, "yes"),
    ("Intern", 9, "no"),
    ("Manager", 20, "yes"),
    ("Staff", 0, "no"),
]


@pytest.mark.parametrize("position,hours,is_weekend", CASES)
def test_overtime(exercise_path, position, hours, is_weekend):
    context = f"input position={position!r}, hours={hours}, is_weekend={is_weekend!r}"
    inputs = f"{position}\n{hours}\n{is_weekend}\n"
    output = run_exercise(exercise_path, inputs)
    (pay,) = read_numbers(output, 1, context)

    expected = overtime(position, hours, is_weekend)
    assert round(pay, 2) == round(expected, 2), f"{context} -> overtime_pay expected {round(expected, 2)} but got {round(pay, 2)}"
