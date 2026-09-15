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


def tax(name, base_salary, overtime_hours, status):
    gross = base_salary + overtime_hours * 35
    if status == "Single":
        rate = 0.22 if gross >= 5000 else 0.18
    elif status == "Married":
        rate = 0.20 if gross >= 6000 else 0.15
    else:  # Head
        rate = 0.25 if gross >= 5500 else 0.19
    net = gross - gross * rate - gross * 0.11 - gross * 0.005
    return rate, net


CASES = [
    ("Ali", 4000.0, 40, "Single"),
    ("Siti", 3000.0, 0, "Single"),
    ("Bob", 5000.0, 40, "Married"),
    ("Chong", 4000.0, 0, "Married"),
    ("Zara", 5000.0, 20, "Head"),
    ("Meng", 3000.0, 10, "Head"),
    ("Devi", 6000.0, 0, "Married"),
    ("Kumar", 5500.0, 0, "Head"),
    ("Lina", 4500.0, 20, "Single"),
    ("Sam", 2000.0, 0, "Head"),
]


@pytest.mark.parametrize("name,base_salary,overtime_hours,status", CASES)
def test_tax(exercise_path, name, base_salary, overtime_hours, status):
    context = f"input name={name!r}, base={base_salary}, overtime={overtime_hours}, status={status!r}"
    inputs = f"{name}\n{base_salary}\n{overtime_hours}\n{status}\n"
    output = run_exercise(exercise_path, inputs)
    line1, line2, line3 = read_lines(output, 3, context)

    exp_rate, exp_net = tax(name, base_salary, overtime_hours, status)

    assert line1 == name, f"{context} -> name expected {name!r} but got {line1!r}"
    try:
        got_rate = float(line2)
    except ValueError:
        pytest.fail(f"{context} -> tax_rate must be a number but got {line2!r}")
    assert round(got_rate, 4) == round(exp_rate, 4), f"{context} -> tax_rate expected {exp_rate} but got {line2!r}"
    try:
        got_net = float(line3)
    except ValueError:
        pytest.fail(f"{context} -> net_salary must be a number but got {line3!r}")
    assert round(got_net, 2) == round(exp_net, 2), f"{context} -> net_salary expected {round(exp_net, 2)} but got {line3!r}"
