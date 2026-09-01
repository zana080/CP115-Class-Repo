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


def read_lines(output, count, context):
    lines = output.replace("\r\n", "\n").strip().split('\n') if output.strip() else []
    if len(lines) != count:
        pytest.fail(
            f"{context}: expected {count} line(s) of output but got {len(lines)}. "
            f"Actual output: {output!r}"
        )
    return lines


CASES = [
    ("Ali", 30.0, 4, "yes"),
    ("siti binti ahmad", 99.99, 1, "no"),
    ("Bob", 50.0, 2, "yes"),
    ("chong", 100.0, 1, "no"),
    ("Zara", 25.5, 3, "yes"),
]


@pytest.mark.parametrize("name,price,quantity,member_answer", CASES)
def test_order_summary(exercise_path, name, price, quantity, member_answer):
    context = f"input name={name!r}, price={price}, quantity={quantity}, member={member_answer!r}"
    inputs = f"{name}\n{price}\n{quantity}\n{member_answer}\n"
    output = run_exercise(exercise_path, inputs)
    line1, line2, line3, line4 = read_lines(output, 4, context)

    order_total = price * quantity
    exp_name = name.upper()
    exp_free = "True" if order_total >= 100 else "False"
    exp_member = "True" if member_answer == "yes" else "False"

    assert line1 == exp_name, f"{context} -> name expected {exp_name!r} but got {line1!r}"
    assert round(float(line2), 2) == round(order_total, 2), f"{context} -> order total expected {round(order_total, 2)} but got {line2!r}"
    assert line3 == exp_free, f"{context} -> free shipping expected {exp_free!r} but got {line3!r}"
    assert line4 == exp_member, f"{context} -> member expected {exp_member!r} but got {line4!r}"
