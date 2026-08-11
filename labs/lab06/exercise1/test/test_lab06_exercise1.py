import pytest
import subprocess
import sys
import os


@pytest.fixture
def exercise_path():
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'exercise1.py')


def run_exercise(exercise_path):
    if not os.path.isfile(exercise_path):
        pytest.fail("exercise1.py was not found in the exercise1 folder")

    process = subprocess.Popen(
        [sys.executable, exercise_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    stdout, stderr = process.communicate(input="")

    if process.returncode != 0:
        error = stderr.strip().splitlines()[-1] if stderr.strip() else "the program crashed"
        pytest.fail(f"the program did not run: {error}")

    return stdout


# The exact receipt the program must print. Tabs are real \t characters.
EXPECTED = (
    "========== RECEIPT ==========\n"
    "Item\t\tPrice\tQty\tTotal\n"
    "Coffee\t\t$3.50\t2\t$7.00\n"
    "Muffin\t\t$2.10\t3\t$6.30\n"
    "Water\t\t$1.05\t4\t$4.20\n"
    "------------------------------\n"
    "Subtotal\t\t\t$17.50\n"
    "Tax (6%)\t\t\t$1.05\n"
    "Total\t\t\t$18.55\n"
    "============================"
)


def test_receipt_output(exercise_path):
    output = run_exercise(exercise_path).replace("\r\n", "\n").rstrip("\n")

    assert output == EXPECTED, (
        "the receipt does not match exactly. "
        f"expected {EXPECTED!r} but got {output!r}"
    )
