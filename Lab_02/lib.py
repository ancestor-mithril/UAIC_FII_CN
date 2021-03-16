import itertools

import numpy as np
import functions as ff


def cholesky_decomposition(a):
    n = len(a)
    l_matrix = [[0 for i in range(n)] for j in range(n)]

    for i in range(n):
        for j in range(i + 1):
            value = a[i][j]
            if j == i:
                for k in range(j):
                    value -= l_matrix[j][k] ** 2
                if value < 0:
                    raise Exception("Matrix is not positive 1")
                l_matrix[i][j] = np.sqrt(value)  # int(np.sqrt(value))
            else:
                for k in range(j):
                    value -= l_matrix[i][k] * l_matrix[j][k]
                if value == 0:
                    raise Exception("Matrix is not positive 2")
                value /= l_matrix[j][j]
                l_matrix[i][j] = value  # int(value)
    return l_matrix


def determ_A(a):
    l = cholesky_decomposition(a)
    det_l = 1
    for i in range(len(l)):
        det_l *= l[i][i]
    return det_l ** 2


def system_solve(a, b):
    """
    deci aicae x[j] da un warning, si am incercat sa rezolv chestia asta exact asa cum ii in pdf la pagina 5. cred ca in mare e corect, verifica tu
    """
    l = cholesky_decomposition(a)
    # A = L * Lt
    # Ax = b => L * Lt * x = b

    # 1. L * y = b
    n = len(l)
    y = [0 for i in range(n)]
    for i in range(n):
        value = b[i]
        for j in range(i + 1):
            if i == j:
                y[j] = value / l[i][j]
            else:
                value -= l[i][j] * y[j]

    # 2. Lt * x = y
    # j -> [i+1,n]
    x = [0 for i in range(n)]
    for i in range(n - 1, -1, -1):
        value = y[i]
        for j in range(n - 1, i - 1, -1):
            value -= l[j][i] * x[j]
        x[j] = value / l[i][i]
    return x


def bonus(a, b):
    a_vec = [a[x][i] for x in range(len(a)) for i in range(x, len(a))]
    print("a_vec", "\n", a_vec, "\n")

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

    l = bonus_cholesky_decomposition(a_vec)
    print("l", "\n", l, "\n")
    n = int((len(l) * 2) ** 0.5)
    y = [0 for i in range(n)]
    for i in range(n):
        value = b[i]
        for j in range(i + 1):
            if i == j:
                y[j] = value / l[matrix_to_vector(i, j, n)]
            else:
                value -= l[matrix_to_vector(i, j, n)] * y[j]

    x = [0 for i in range(n)]
    for i in range(n - 1, -1, -1):
        value = y[i]
        for j in range(n - 1, i - 1, -1):
            value -= l[matrix_to_vector(j, i, n)] * x[j]
        x[j] = value / l[matrix_to_vector(i, i, n)]
    print(x)





