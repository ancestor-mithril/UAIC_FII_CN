import unittest
import numpy as np
import scipy
import scipy.linalg
import random
import lib
import functions as ff


class CholeskyDecomposition(unittest.TestCase):
    m1 = [[4, 2, 8], [2, 10, 10], [8, 10, 21]]
    A = [
        [2.25, 3, 3],
        [3, 9.0625, 13],
        [3, 13, 24]
    ]
    b = [9, 35.0625, 61]
    x = [0, 1, 2]

    def test_1_decomp(self):

        cd = CholeskyDecomposition

        A = np.array(cd.m1)
        L = scipy.linalg.cholesky(A, lower=True)
        U = scipy.linalg.cholesky(A, lower=False)

        res = lib.cholesky_decomposition(cd.m1)
        np.testing.assert_array_almost_equal(res, L)

    def test_2_determA(self):
        cd = CholeskyDecomposition

        det = lib.determ_A(cd.m1)

        np.testing.assert_array_almost_equal(np.linalg.det(cd.m1), det)

    def test_3_X_chol(self):
        cd = CholeskyDecomposition

        let = lib.system_solve(cd.A, cd.b)
        let2 = np.linalg.solve(cd.A, cd.b)
        np.testing.assert_array_almost_equal(let, let2)

    def test_4_tsolve(self):
        cd = CholeskyDecomposition

        x_chol = lib.system_solve(cd.A, cd.b)
        a_x_chol = ff.get_matrix_mul(cd.A, x_chol)
        err = 0

        for i in range(len(a_x_chol)):
            err += (a_x_chol[i] - cd.b[i]) ** 2
        err = err ** 0.5

        aux = np.subtract(a_x_chol, cd.b)
        self.assertAlmostEqual(np.linalg.norm(aux, 2), err)

    def test_5_lu(self):
        cd = CholeskyDecomposition

        p, l, u = scipy.linalg.lu(cd.A)
        print(p, l, u)
        x = np.linalg.solve(cd.A, cd.b)
        print(x)
        self.assertTrue(True)

    def test_6_inverse(self):
        cd = CholeskyDecomposition

        if ff.get_matrix_determinant(cd.A) == 0:
            raise Exception("Invalid matrix")
        inv = ff.get_matrix_inverse(cd.A)
        inv2 = np.linalg.inv(cd.A)
        np.testing.assert_array_almost_equal(inv, inv2)


def read_from_file():
    A = eval(open("A.txt", "r").read())
    b = eval(open("b.txt", "r").read())
    return A, b


def read_from_stdin():
    print(
        "Se presupune ca utilizatorul introduce date corecte, dimensiunea matricii un int, si fiecare element un float"
    )
    n = int(input("Introdu dimensiunea matricii A:"))
    A = []
    for i in range(n):
        line = []
        for j in range(n):
            x = float(input(f"Introdu elementul de pe linia {i}, coloana {j}"))
            line.append(x)
        A.append(line)
    print(A)
    print("Citeste valorile din b")
    b = []
    for i in range(n):
        x = float(input(f"Introdu elementul {i} din b"))
        b.append(x)
    CholeskyDecomposition.A = A
    CholeskyDecomposition.m1 = CholeskyDecomposition.A
    CholeskyDecomposition.b = b


def random_init(n):
    def matrix_to_vector(i, j, n):
        if i <= j:
            return int(i * n - (i - 1) * i / 2 + j - i)
        return int(j * n - (j - 1) * j / 2 + i - j)

    while True:
        v = [random.randint(-1000, 1000) for i in range(n * (n + 1 // 2))]
        A = [[v[matrix_to_vector(i, j, n) if j >= i else 0] for i in range(n)] for j in range(n)]
        for i in range(n):
            for j in range(i):
                A[i][j] = A[j][i]
        b = [random.randint(-10, 10) for _ in range(n)]
        try:
            lib.cholesky_decomposition(A)
            return A, b
        except Exception as e:
            print(e)
            pass





if __name__ == "__main__":

    unittest.main()

