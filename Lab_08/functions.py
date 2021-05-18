import random


h = 10 ** (-6)
epsilon = 10 ** (-8)


def read_f(path: str = "f.txt") -> callable:
    exec_dict = {}
    exec(open(path, "r").read(), locals(), exec_dict)
    if len(exec_dict.values()) > 0:
        f = list(exec_dict.values())[0]
    else:
        raise Exception(f"no function in {path}")
    return f


def dehghan_hajarian(f: callable, iterations: int = 100):
    global epsilon
    x = random.uniform(-100, 100)
    delta_x = 0
    for _ in range(iterations):
        g_x = get_df(f, x)
        g_x_plus_gx = get_df(f, x + g_x)
        if abs(g_x_plus_gx - g_x) <= epsilon:
            return x
        z = x + (g_x ** 2) / (g_x_plus_gx - g_x)
        delta_x = (g_x * (get_df(f, z) - g_x)) / (g_x_plus_gx - g_x)
        x = x - delta_x
        if delta_x <= epsilon or delta_x >= (10 ** 8):
            break
    if delta_x <= epsilon:
        return x
    print("Divergent")
    return None


def get_df(f: callable, x: float) -> float:
    global h
    # return g1(f, x, h)
    return g2(f, x, h)


def g1(f: callable, x: float, h: float) -> float:
    return (3 * f(x) - 4 * f(x - h) + f(x - 2 * h)) / (2 * h)


def g2(f: callable, x: float, h: float) -> float:
    return (-f(x + 2 * h) + 8 * f(x + h) - 8 * f(x - h) + f(x - 2 * h)) / (12 * h)


def get_d2f(f: callable, x: float) -> float:
    global h
    return (-f(x + 2 * h) + 16 * f(x + h) - 30 * f(x) + 16 * f(x-h) - f(x - 2 * h)) / (12 * h * h)
