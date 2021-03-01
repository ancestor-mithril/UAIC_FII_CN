def get_matrix_mul(matrix_1, matrix_2):
    is_mat_2_lst = isinstance(matrix_2[0], list)
    len_lst = len(matrix_2[0]) if is_mat_2_lst else 1
    if is_mat_2_lst:
        matrix_3 = [[0 for y in range(len_lst)] for y in range(len(matrix_1))]
    else:
        matrix_3 = [0 for y in range(len(matrix_1))]
    for i in range(len(matrix_1)):
        for j in range(len_lst):
            for k in range(len(matrix_2)):
                if is_mat_2_lst:
                    matrix_3[i][j] += matrix_1[i][k] * matrix_2[k][j]
                else:
                    matrix_3[i] += matrix_1[i][k] * matrix_2[k]
    return matrix_3


def get_matrix_minor(m, i, j):
    return [row[:j] + row[j + 1:] for row in (m[:i] + m[i + 1:])]


def get_matrix_determinant(m):
    if len(m) == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1) ** c) * m[0][c] * get_matrix_determinant(get_matrix_minor(m, 0, c))
    return determinant


def get_matrix_transpose(m):
    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]


def get_matrix_cofactor(m):
    return [[(-1)**(x+y) * get_matrix_determinant(get_matrix_minor(m, x, y)) for y in range(3)] for x in range(3)]


def get_matrix_adjugate(m):
    return get_matrix_transpose(get_matrix_cofactor(m))


def get_matrix_inverse(m):
    det = get_matrix_determinant(m)
    adj = get_matrix_adjugate(m)
    return [[adj[x][y] / det for y in range(3)] for x in range(3)]
