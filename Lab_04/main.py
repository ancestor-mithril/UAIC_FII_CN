import json

epsilon = 10**(-8)


def read_tridiag(path: str):
    with open(path, "r") as f:
        lines = f.readlines()
    n, q, p = [int(lines[i]) for i in range(3)]
    a, b, c = [[], [], []]
    for ln in lines[3:]:
        try:
            x = float(ln.strip('\n'))
        except:
            continue
        if len(a) < n:
            if x == 0:
                raise Exception("invalid diag")
            a.append(x)
        elif len(c) < n - p:
            c.append(x)
        elif len(b) < n - q:
            b.append(x)
    return {"a": a, "b": b, "c": c, "n": n, "p": p, "q": q}


def read_arr(path: str):
    with open(path, "r") as f:
        lines = f.readlines()
    n = int(lines[0])
    arr = []
    for ln in lines[1:]:
        try:
            x = float(ln.strip('\n'))
        except:
            continue
        arr.append(x)
    return arr


def gauss_seidel(mat, f, x):
    a, b, c = mat['a'], mat['b'], mat['c']
    n, q, p = mat['n'], mat['q'], mat['p']
    x.append(0)
    a.append(0)
    b.append(0)
    c.append(0)
    for i in range(n):
        i1 = i - q if i - q > 0 else -1
        i2 = i
        i3 = i + p if i + p < n else -1
        x[i2] = (f[i] - c[i1] * x[i1] - b[i3] * x[i3]) / a[i2]
        if x[i2] > 10**3:
            x[i2] = 10**3
    x.pop()
    a.pop()
    b.pop()
    c.pop()


def too_far_apart(a, b):
    return not (a - b > 10 ** 8 or b - a > 10 ** 8)


def norm_euclid(x, xp):
    return sum((x[i] - xp[i])**2 if too_far_apart(x[i], xp[i]) else 10**2 for i in range(len(x)))


def norm_inform(x, xp):
    return abs(max([x[i] - xp[i] if too_far_apart(x[i], xp[i]) else 10**2 for i in range(len(x))]))


def solve_pr(mat, f):
    n = mat['n']
    x = [0 for _ in range(n)]
    for it in range(10000):
        xp = json.loads(json.dumps(x))
        gauss_seidel(mat, f, x)
        if norm_euclid(x, xp) < epsilon:
            return x, True
    return x, False


def tridiag_x_vector(mat, x):
    resx = []
    for i in range(mat['n']):
        y = mat['a'][i] * x[i]
        if i - mat['p'] > 0:
            y += mat['b'][i - mat['p']] * x[i - mat['p']]
        if i + mat['q'] < mat['n']:
            y += mat['c'][i] * x[i + mat['q']]
        resx.append(y)
    return resx


if __name__ == '__main__':
    a_s = [read_tridiag("a" + str(i+1) + ".txt") for i in range(5)]
    f_s = [read_arr("f" + str(i+1) + ".txt") for i in range(5)]
    for ex in range(5):
        x, res = solve_pr(a_s[ex], f_s[ex])
        y = tridiag_x_vector(a_s[ex], x)
        print(norm_inform(y, f_s[ex]))
