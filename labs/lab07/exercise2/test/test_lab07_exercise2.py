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


@pytest.mark.parametrize("amount", [50, 137, 200, 49, 0, 99, 350, 1, 500, 251])
def test_bank_notes(exercise_path, amount):
    context = f"input amount={amount}"
    output = run_exercise(exercise_path, f"{amount}\n")
    notes, coins = read_numbers(output, 2, context)

    exp_notes = amount // 50
    exp_coins = amount % 50

    assert int(notes) == exp_notes, f"{context} -> notes expected {exp_notes} but got {int(notes)}"
    assert int(coins) == exp_coins, f"{context} -> coins expected {exp_coins} but got {int(coins)}"
