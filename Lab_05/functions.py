import json
import numpy as np


epsilon = 10e-13


def read_matrix(path: str = "a.txt"):
    return eval(open(path, "r").read())


def ex_1(a):

    n = len(a)
    a_vec = [a[x][i] for x in range(n) for i in range(x, n)]

    def matrix_to_vector(i, j, n):
        if i <= j:
            return int(i * n - (i - 1) * i / 2 + j - i)
        return int(j * n - (j - 1) * j / 2 + i - j)

    def jacobi_alg(a_vec, iterations=10000):
        k = 0
        u = [[1 if i == j else 0 for i in range(n)] for j in range(n)]
        for _ in range(iterations):
            p, q = get_pq(a_vec)
            if a_vec[matrix_to_vector(p, q, n)] < epsilon:
                break
            c, s, t = get_cst(a_vec, p, q)
            a_vec = modify_a(a_vec, p, q, c, s, t)
            u = modify_u(u, p, q, c, s)
        return a_vec, [a_vec[matrix_to_vector(i, i, n)] for i in range(n)], u

    def get_pq(a_vec):
        p = 0
        q = 1
        magnus = a_vec[matrix_to_vector(p, q, n)]
        for i in range(1, n):
            for j in range(i):
                x = abs(a_vec[matrix_to_vector(i, j, n)])
                if magnus < x:
                    magnus = x
                    p = i
                    q = j
        return p, q

    def get_cst(a_vec, p, q):
        alpha = (a_vec[matrix_to_vector(p, p, n)] - a_vec[matrix_to_vector(q, q, n)]) / \
                (2 * a_vec[matrix_to_vector(p, q, n)])
        sign = 1 if alpha > 0 else -1
        t = -alpha + sign * ((alpha ** 2 + 1) ** 0.5)
        c = 1 / ((1 + t ** 2) ** 0.5)
        s = t / ((1 + t ** 2) ** 0.5)
        return c, s, t

    def modify_a(a_vec, p, q, c, s, t):
        for j in range(n):
            if j == p or j == q:
                continue
            a_vec[matrix_to_vector(p, j, n)] = c * a_vec[matrix_to_vector(p, j, n)] \
                                               + s * a_vec[matrix_to_vector(q, j, n)]
            a_vec[matrix_to_vector(q, j, n)] = -s * a_vec[matrix_to_vector(j, p, n)] \
                                               + c * a_vec[matrix_to_vector(q, j, n)]
        a_vec[matrix_to_vector(p, p, n)] += t * a_vec[matrix_to_vector(p, q, n)]
        a_vec[matrix_to_vector(p, p, n)] -= t * a_vec[matrix_to_vector(p, q, n)]
        a_vec[matrix_to_vector(p, q, n)] = 0
        return a_vec

    def modify_u(u, p, q, c, s):
        for i in range(n):
            aux = u[i][p]
            u[i][p] = c * u[i][p] + s * u[i][q]
            u[i][q] = -s * aux + c * u[i][q]
        return u

    def a_vec_x_u(a_vec, u):
        rez = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                s = 0
                for k in range(n):
                    s += a_vec[matrix_to_vector(i, k, n)] * u[k][j]
                rez[i][j] = s
        return rez

    def u_x_a_diag(u, a_diag):
        rez = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                rez[i][j] = u[i][i] * a_diag[j]
        return rez

    def l_1_norm(a_1, a_2):
        m = (np.subtract(a_1, a_2)).tolist()
        return max(sum([abs(x) for x in line]) for line in m)

    a_vec, a_diag, u = jacobi_alg(a_vec)
    print("a_vec")
    print(a_vec)
    print('\n')
    print("a_diag")
    print(a_diag)
    print('\n')
    print("u")
    print(u)
    print('\n')
    a_vec = [a[x][i] for x in range(n) for i in range(x, n)]
    rez1 = a_vec_x_u(a_vec, u)
    rez2 = u_x_a_diag(u, a_diag)
    print("a_vec_x_u")
    print(rez1)
    print('\n')
    print("u_x_a_diag")
    print(rez2)
    print('\n')
    norm = l_1_norm(rez1, rez2)
    print("norm")
    print(norm)
    print('\n')


def ex_2(a, iterations: int = 100):
    a_vec = [a[x][i] for x in range(len(a)) for i in range(x, len(a))]

    def matrix_to_vector(i, j, n):
        if i <= j:
            return int(i * n - (i - 1) * i / 2 + j - i)
        return int(j * n - (j - 1) * j / 2 + i - j)

    def bonus_cholesky_decomposition(a):
        n = int((len(a) * 2) ** 0.5)
        l_vec = [0 for i in range(n * (n + 1) // 2)]
        for i in range(n):
            for j in range(i + 1):
                value = a[matrix_to_vector(i, j, n)]
                if j == i:
                    for k in range(j):
                        value -= l_vec[matrix_to_vector(j, k, n)] ** 2
                    if value < 0:
                        raise Exception("Matrix is not positive 2")
                    l_vec[matrix_to_vector(i, j, n)] = np.sqrt(value)  # int(np.sqrt(value))
                else:
                    for k in range(j):
                        value -= l_vec[matrix_to_vector(i, k, n)] * l_vec[matrix_to_vector(j, k, n)]
                    if value == 0:
                        raise Exception("Matrix is not positive 1")
                    value /= l_vec[matrix_to_vector(j, j, n)]
                    l_vec[matrix_to_vector(i, j, n)] = value  # int(value)
        return l_vec

    def norm_l1(a_1, a_2):
        n = int((len(a_1) * 2) ** 0.5)
        m = [a_1[i] - a_2[i] for i in range(len(a_1))]
        m = [[m[matrix_to_vector(i, j, n)] for i in range(n)] for j in range(n)]
        return max(sum([abs(x) for x in line]) for line in m)

    def recalculate_a_using_l(l_vec):
        n = int((len(l_vec) * 2) ** 0.5)
        rez = [0 for _ in range(len(l_vec))]
        for i in range(n):
            for j in range(n):
                s = 0
                for ik in range(i, n):
                    if ik >= j:
                        s += l_vec[matrix_to_vector(i, ik, n)] * l_vec[matrix_to_vector(ik, j, n)]
                rez[matrix_to_vector(i, j, n)] = s
        return rez

    for _ in range(iterations):
        l_vec = bonus_cholesky_decomposition(a_vec)
        a_copy = json.loads(json.dumps(a_vec))
        a_vec = recalculate_a_using_l(l_vec)
        if norm_l1(a_copy, a_vec) < epsilon:
            break

    print("a_vec")
    print(a_vec)


def ex_3(a, iterations: int = 100):
    u, s, vt = np.linalg.svd(a)
    print("Singular Value Decomposition")
    print("U")
    print(u)
    print("\n")
    print("S")
    print(s)
    print("\n")
    print("Vt")
    print(vt)
    ss = [i for i in s if i != 0]
    print("\n")
    print(f"Rang A = {len(ss)}")
    print("\n")
    print(f"k2(A) = {max(ss) / min(ss)}")

    def get_transpose(m):
        return [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]

    def matrix_mul(a1, a2):
        rez = [[0 for _ in range(len(a2[0]))] for _ in range(len(a1))]
        for i in range(len(a1)):
            for j in range(len(a2[0])):
                s = 0
                for k in range(len(a1[0])):
                    s += a1[i][k] * a2[k][j]
                rez[i][j] = s
        return rez

    def l_1_norm(a_1, a_2):
        m = (np.subtract(a_1, a_2)).tolist()
        return max(sum([abs(x) for x in line]) for line in m)

    p = len(u)
    n = len(vt)
    si = [[0 if j != i or i >= len(ss) else ss[i] for j in range(p)] for i in range(n)]
    ai = matrix_mul(matrix_mul(get_transpose(vt), si), get_transpose(u))
    print("Ai = VSUt")
    print(ai)
    print("\n")
    aj = np.dot(np.linalg.inv(np.dot(np.transpose(a), np.array(a))), np.transpose(a))
    aj = [[aj[i, j] for j in range(aj.shape[1])] for i in range(aj.shape[0])]
    print(f"||Ai - Aj||1 = {l_1_norm(aj, ai)}")
    print()
    pass

