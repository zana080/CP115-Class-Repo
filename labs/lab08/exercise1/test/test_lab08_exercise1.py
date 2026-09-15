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


def classify(gpa, credit_hours):
    if gpa >= 3.8 and credit_hours >= 12:
        return "Dean's List"
    elif gpa >= 3.5 and credit_hours >= 12:
        return "Honor Roll"
    elif gpa >= 2.0:
        return "Good Standing"
    else:
        return "Academic Probation"


CASES = [
    ("Ali", 3.9, 15),
    ("Siti", 3.6, 12),
    ("Bob", 3.9, 9),
    ("Chong", 2.5, 18),
    ("Zara", 1.8, 15),
    ("Meng", 3.5, 11),
    ("Devi", 4.0, 12),
    ("Kumar", 2.0, 6),
    ("Lina", 3.7, 20),
    ("Sam", 1.0, 3),
]


@pytest.mark.parametrize("name,gpa,credit_hours", CASES)
def test_classification(exercise_path, name, gpa, credit_hours):
    context = f"input name={name!r}, gpa={gpa}, credit_hours={credit_hours}"
    inputs = f"{name}\n{gpa}\n{credit_hours}\n"
    output = run_exercise(exercise_path, inputs)
    (line1,) = read_lines(output, 1, context)

    expected = classify(gpa, credit_hours)
    assert line1 == expected, f"{context} -> classification expected {expected!r} but got {line1!r}"
