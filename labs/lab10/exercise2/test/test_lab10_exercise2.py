import pytest
import subprocess
import sys
import os


@pytest.fixture
def exercise_path():
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'exercise2.py')


def run_exercise(exercise_path, inputs):
    if not os.path.isfile(exercise_path):
        pytest.fail("exercise2.py was not found in the exercise2 folder")

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


def temperature_monitor(threshold, temps):
    danger = sum(1 for t in temps if t > threshold)
    average = sum(temps) / len(temps)
    return danger, average


CASES = [
    (35.0, [32, 37, 34, 39]),
    (30.0, [25, 28, 29]),
    (30.0, [31, 32, 33]),
    (37.5, [37.5, 38.0, 36.0]),
    (20.0, [22, 18, 25, 19, 30]),
    (40.0, [39, 41]),
    (25.0, [25, 25, 25]),
    (33.0, [30, 34, 31, 35, 32, 36]),
    (28.0, [28]),
    (15.0, [16, 17, 18, 19]),
]


@pytest.mark.parametrize("threshold,temps", CASES)
def test_temperature_monitor(exercise_path, threshold, temps):
    context = f"input days={len(temps)}, threshold={threshold}, temps={temps}"
    inputs = f"{len(temps)}\n{threshold}\n" + "".join(f"{t}\n" for t in temps)
    output = run_exercise(exercise_path, inputs)
    line1, line2 = read_lines(output, 2, context)

    exp_danger, exp_avg = temperature_monitor(threshold, temps)

    assert line1 == str(exp_danger), f"{context} -> danger days expected {exp_danger} but got {line1!r}"
    assert round(float(line2), 1) == round(exp_avg, 1), f"{context} -> average temperature expected {round(exp_avg, 1)} but got {line2!r}"
