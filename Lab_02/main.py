import unittest
import numpy as np
import scipy
import scipy.linalg

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
            err += (a_x_chol[i] - cd.b[i])**2
        err = err ** 0.5

        aux = np.add(a_x_chol, np.multiply(-1, cd.b))
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

        print("norm", np.linalg.norm(np.subtract(inv, inv2)))


if __name__ == "__main__":
    unittest.main()