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


MAIN = {"Chicken": 10, "Beef": 12, "Fish": 11}
DRINK = {"Soft Drink": 2, "Coffee": 3}
DESSERT = {"Ice Cream": 4, "Cake": 5}


def restaurant(main, drink, dessert):
    food = MAIN[main] + DRINK[drink] + DESSERT[dessert]
    bill = food + food * 0.10
    return bill


CASES = [
    ("Chicken", "Soft Drink", "Ice Cream"),
    ("Beef", "Coffee", "Cake"),
    ("Fish", "Soft Drink", "Cake"),
    ("Chicken", "Coffee", "Ice Cream"),
    ("Beef", "Soft Drink", "Cake"),
    ("Fish", "Coffee", "Ice Cream"),
    ("Chicken", "Soft Drink", "Cake"),
    ("Beef", "Coffee", "Ice Cream"),
    ("Fish", "Soft Drink", "Ice Cream"),
    ("Chicken", "Coffee", "Cake"),
]


@pytest.mark.parametrize("main,drink,dessert", CASES)
def test_restaurant(exercise_path, main, drink, dessert):
    context = f"input main={main!r}, drink={drink!r}, dessert={dessert!r}"
    inputs = f"{main}\n{drink}\n{dessert}\n"
    output = run_exercise(exercise_path, inputs)
    (bill,) = read_numbers(output, 1, context)

    expected = restaurant(main, drink, dessert)
    assert round(bill, 2) == round(expected, 2), f"{context} -> final_bill expected {round(expected, 2)} but got {round(bill, 2)}"
