import random
from typing import List


epsilon = 10e-8


def read_polynomial(input_path : str = "input.txt"):
    return eval(open(input_path, "r").read())


def evaluate_r(a: List[int]) -> float:
    return abs((abs(a[-1]) + max(a)) / abs(a[-1]))


def evaluate_polynomial(a: List[int], x: float):
    return sum([a[i] * (x ** i) for i in range(len(a))])


def evaluate_polynomial_d1(a: List[int], x: float):
    return sum([a[i] * i * (x ** (i - 1)) for i in range(1, len(a))])


def evaluate_polynomial_d2(a: List[int], x: float):
    return sum([a[i] * i * (i - 1) * (x ** (i-2)) for i in range(2, len(a))])


def olver_method(max_iterations: int = 1000):
    global epsilon
    a = read_polynomial()
    r = evaluate_r(a)
    x = random.uniform(-r, r)
    k = 0
    delta_x = 10 ** 7
    for _ in range(max_iterations):
        pd1 = evaluate_polynomial_d1(a, x)
        if abs(pd1) <= epsilon:
            break
        p = evaluate_polynomial(a, x)
        pd2 = evaluate_polynomial_d2(a, x)
        c = (p ** 2) * pd2 / (pd1 ** 3)
        delta_x = p / pd1 + 0.5 * c
        x = x - delta_x
        k += 1
        if delta_x <= epsilon or delta_x >= (10 ** 8):
            break
    if delta_x < epsilon:
        return True, x
    return False, x


def repeat_olver(iterations : int = 30):
    for i in range(iterations):
        ok, result = olver_method(100)
        print(f"Iteration {i}: {ok}, {result}")
        if ok:
            break
