import pytest
import subprocess
import sys
import os


@pytest.fixture
def exercise_path():
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'exercise4.py')


def run_exercise(exercise_path, inputs):
    if not os.path.isfile(exercise_path):
        pytest.fail("exercise4.py was not found in the exercise4 folder")

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


def cafe_bill(dp, dq, cp, cq):
    subtotal = dp * dq + cp * cq
    service_charge = subtotal * 0.10
    final = subtotal + service_charge - 2
    return subtotal, service_charge, final


CASES = [
    (5.00, 2, 8.00, 1),
    (3.50, 4, 6.20, 3),
    (10.00, 1, 0.00, 0),
    (4.90, 5, 12.30, 2),
    (2.00, 3, 2.00, 3),
]


@pytest.mark.parametrize("dp,dq,cp,cq", CASES)
def test_cafe_bill(exercise_path, dp, dq, cp, cq):
    context = f"input {dp},{dq},{cp},{cq}"
    inputs = f"{dp}\n{dq}\n{cp}\n{cq}\n"
    output = run_exercise(exercise_path, inputs)
    subtotal, service_charge, final = read_numbers(output, 3, context)

    exp_subtotal, exp_service, exp_final = cafe_bill(dp, dq, cp, cq)

    assert round(subtotal, 2) == round(exp_subtotal, 2), f"{context} -> subtotal expected {round(exp_subtotal, 2)} but got {round(subtotal, 2)}"
    assert round(service_charge, 2) == round(exp_service, 2), f"{context} -> service charge expected {round(exp_service, 2)} but got {round(service_charge, 2)}"
    assert round(final, 2) == round(exp_final, 2), f"{context} -> final expected {round(exp_final, 2)} but got {round(final, 2)}"
