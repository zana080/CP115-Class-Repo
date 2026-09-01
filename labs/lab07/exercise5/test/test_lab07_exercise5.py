import pytest
import subprocess
import sys
import os


@pytest.fixture
def exercise_path():
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'exercise5.py')


def run_exercise(exercise_path, inputs):
    if not os.path.isfile(exercise_path):
        pytest.fail("exercise5.py was not found in the exercise5 folder")

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


CASES = [
    ("Ali Bin Abu", "secret12", "kuala lumpur", "tokyo"),
    ("Sara", "abc", "penang", "bangkok"),
    ("chong wei", "password", "johor", "singapore"),
    ("Maria Lopez", "12345678", "manila", "dubai"),
    ("Tan", "short", "ipoh", "seoul"),
]


@pytest.mark.parametrize("name,password,origin,destination", CASES)
def test_travel_account(exercise_path, name, password, origin, destination):
    context = f"input name={name!r}, password={password!r}, origin={origin!r}, destination={destination!r}"
    inputs = f"{name}\n{password}\n{origin}\n{destination}\n"
    output = run_exercise(exercise_path, inputs)
    line1, line2, line3, line4 = read_lines(output, 4, context)

    exp_username = name.lower()
    exp_length = str(len(name))
    exp_long = "True" if len(password) >= 8 else "False"
    exp_route = origin.upper() + "-" + destination.upper()

    assert line1 == exp_username, f"{context} -> username expected {exp_username!r} but got {line1!r}"
    assert line2 == exp_length, f"{context} -> name length expected {exp_length!r} but got {line2!r}"
    assert line3 == exp_long, f"{context} -> long enough expected {exp_long!r} but got {line3!r}"
    assert line4 == exp_route, f"{context} -> route expected {exp_route!r} but got {line4!r}"
