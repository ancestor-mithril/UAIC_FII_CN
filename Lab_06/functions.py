import json
import random
from math import sin, cos
from typing import List
import numpy as np
from matplotlib import pyplot as plt

epsilon = 10e-8


def get_function_domain(file_path: str = "input_01.txt"):
    n, x0, xn = read_x0_xn(file_path)
    assert x0 < xn, f"{x0} < {xn} == false"
    n = int(n)
    x = [x0]
    for _ in range(n - 2):
        x.append(random.uniform(x0 + epsilon, xn - epsilon))
    x.append(xn)
    x = sorted(x)
    return x


def apply_function(x: List[float], function: callable) -> List[float]:
    pass


def function_1(x: float) -> float:
    return x ** 2 - 12 * x + 30


def function_2(x: float) -> float:
    return sin(x) - cos(x)


def function_2_d(x: float) -> float:
    return cos(x) + sin(x)


def function_1_d(x: float) -> float:
    return 2 * x - 12


def read_x0_xn(file_path: str = "input_01.txt"):
    return map(float, eval(open(file_path, "r").read()))


def spline_interpolation(x: List[float], f: callable = function_1, df: callable = function_1_d):
    a = x[0]
    b = x[-1]
    da = df(a)
    while True:
        _x_ = random.uniform(a, b)
        if _x_ not in x:
            break
    A = da
    sfk_list = []
    for i in range(len(x) - 1):
        if x[i] > _x_:
            f_x_ = sfk
        k = random.uniform(x[i] + epsilon, x[i + 1] - epsilon)
        sfk = get_sfk(k, x[i], x[i + 1], A, f)
        sfk_list.append([k, sfk])
        A = get_next_A(A, x[i], x[i + 1], f)

    print(f"_x_ = {_x_}")
    print(f"Sf(_x_) ~= f(_x_) = {f_x_}")
    print(f"|Sf(_x_) - f(_x_)| = {abs(f_x_ - f(_x_))}")
    draw_line([[xi, f(xi)] for xi in x])
    draw_line(sfk_list)


def get_sfk(k: float, xi: float, xi1: float, A: float, f: callable):
    return f(xi) + A * (k - xi) + ((k - xi) ** 2) * ((get_next_A(A, xi, xi1, f) - A) / (2 * (xi1 - xi)))


def get_next_A(A: float, xi: float, xi1: float, f: callable) -> float:
    return -A + 2 * (f(xi1) - f(xi)) / (xi1 - xi)


def get_m_x(x, m):
    y = json.loads(json.dumps(x[1:-1]))
    random.shuffle(y)
    return y[:m]


def min_squares_interpolation(x: List[float], f: callable = function_1, df: callable = function_1_d):
    m = 5
    x_old = x
    x = get_m_x(x, m - 2)
    x.append(x_old[0])
    x.append(x_old[-1])
    x = sorted(x)
    assert m <= 5, "For large matrices this would be too much"
    B = [[xi ** i for i in range(m)] for xi in x]
    y = [f(x_i) for x_i in x]
    a_s = np.linalg.solve(B, y)
    a_s = a_s[::-1]
    while True:
        _x_ = random.uniform(x[0], x[-1])
        if _x_ not in x:
            break
    p_m = horner(a_s, _x_)

    print(f"_x_ = {_x_}")
    print(f"pm(_x_) ~= f(_x_) = {p_m}")
    print(f"|pm(_x_) - f(_x_)| = {abs(p_m - f(_x_))}")
    print("Sum", sum([abs(horner(a_s, xi) - f(xi)) for xi in x]) / len(x))
    draw_line([[xi, f(xi)] for xi in x_old])
    draw_line([[xi, horner(a_s, xi)] for xi in x])


def horner(a, x, level=0):
    if level == len(a) - 1:
        return a[0]
    return a[len(a) - level - 1] + horner(a, x, level + 1) * x


def draw_line(list_of_points):
    x_list = [x for [x, y] in list_of_points]
    y_list = [y for [x, y] in list_of_points]
    plt.plot(x_list, y_list)
    plt.show()
