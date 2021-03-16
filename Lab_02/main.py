from functions import get_matrix_mul, get_matrix_determinant, get_matrix_inverse
from lib import bonus, cholesky_decomposition, determ_A, system_solve
from test import CholeskyDecomposition as cd, read_from_file, random_init
import scipy
import numpy as np

# A, b = random_init(3)  # [[2, 2, 2], [2, 5, 2], [2, 2, 7]]
A, b = read_from_file()  # [[2.25, 3, 3],[3, 9.0625, 13],[3, 13, 24]]
print(A)
L = cholesky_decomposition(A)
print('\n', "ex_1")
print(L)

det = determ_A(A)
print('\n', "ex_2")
print(det)

x = system_solve(A, b)
print('\n', "ex_3")
print(x)

a_x = get_matrix_mul(A, x)


def get_error(a_x, b):
    err = 0
    for i in range(len(a_x)):
        err += (a_x[i] - b[i]) ** 2
    err = err ** 0.5
    return err


print('\n', "ex_4")
print(get_error(a_x, b))

print('\n', "ex_5")
p, l, u = scipy.linalg.lu(A)
print(p, l, u)
x = np.linalg.solve(A, b)
print(x)

print('\n', "ex_6")
if get_matrix_determinant(A) == 0:
    raise Exception("Invalid matrix")

inv = get_matrix_inverse(A)
inv2 = np.linalg.inv(A)
print("norm", np.linalg.norm(np.subtract(inv, inv2)))
# print(inv)
print("\nBONUS\n")
bonus(A, b)
