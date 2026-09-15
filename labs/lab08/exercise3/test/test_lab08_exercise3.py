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


WEEKEND = {"Adult": 18, "Child": 12, "Senior": 15}
WEEKDAY = {"Adult": 15, "Child": 10, "Senior": 12}


def movie(day_type, show_time, customer_type):
    if day_type == "weekend":
        base = WEEKEND[customer_type]
    else:
        base = WEEKDAY[customer_type]
    final = base
    if show_time > 18:
        final = base + 3
    return base, final


CASES = [
    ("weekend", 14, "Adult"),
    ("weekday", 20, "Child"),
    ("weekday", 15, "Senior"),
    ("weekend", 21, "Adult"),
    ("weekday", 19, "Adult"),
    ("weekend", 10, "Senior"),
    ("weekday", 12, "Child"),
    ("weekend", 22, "Child"),
    ("weekday", 18, "Adult"),
    ("weekend", 19, "Senior"),
]


@pytest.mark.parametrize("day_type,show_time,customer_type", CASES)
def test_movie(exercise_path, day_type, show_time, customer_type):
    context = f"input day={day_type!r}, time={show_time}, customer={customer_type!r}"
    inputs = f"{day_type}\n{show_time}\n{customer_type}\n"
    output = run_exercise(exercise_path, inputs)
    base, final = read_numbers(output, 2, context)

    exp_base, exp_final = movie(day_type, show_time, customer_type)

    assert round(base, 2) == round(exp_base, 2), f"{context} -> base_price expected {round(exp_base, 2)} but got {round(base, 2)}"
    assert round(final, 2) == round(exp_final, 2), f"{context} -> final_price expected {round(exp_final, 2)} but got {round(final, 2)}"
