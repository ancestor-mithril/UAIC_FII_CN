import json
import re


def get_line_data(line):
    a = re.sub(" ", "", line).split(",")
    if len(a) == 3:
        return map(float, a)
    return None, None, None


def add_value_to_rare_matrix(rare_matrix, line, col, val):
    line = int(line)
    col = int(col)
    n = len(rare_matrix[line])
    for i in range(n):
        if rare_matrix[line][i][1] == col:
            rare_matrix[line][i][0] += val
            return
    rare_matrix[line].append([val, col])


def read_rare_matrix(path: str = "a.txt"):
    with open(path, "r") as fp:
        lines = fp.readlines()
        matrix_dim = int(lines[0])
        rare_matrix = [[] for i in range(matrix_dim)]
        for i in lines[1:]:
            val, line, col = get_line_data(i)
            if val is not None:
                add_value_to_rare_matrix(rare_matrix, line, col, val)
    return rare_matrix


def read_tridiagonal_matrix(path: str = "b.txt"):
    with open(path, "r") as fp:
        lines = fp.readlines()
        matrix_dim = int(lines[0])
        q_len = int(lines[1])
        p_len = int(lines[2])
        a = []
        b = []
        c = []
        for i in lines[3:]:
            l = i.strip('\n')
            if l == "":
                continue
            if len(a) < matrix_dim:
                a.append(float(l))
            elif len(b) < matrix_dim - q_len:
                b.append(float(l))
            elif len(c) < matrix_dim - p_len:
                c.append(float(l))
    return a, b, c


def sum_rare_with_tridiag_matrix(rare, tridiag):
    a, b, c = tridiag
    q = len(a) - len(b)
    print("q", q)
    p = len(a) - len(c)
    print("p", p)
    rr = json.loads(json.dumps(rare))
    for line in range(len(rare)):
        n = len(rare[line])
        for i in range(n):
            if rr[line][i][1] == line:
                rr[line][i][0] += a[line]
                break
        else:
            rr[line].append([a[line], line])
        bi = b[line] if line < len(b) else None  # ?
        ci = c[line - p] if line >= p else None
        if bi is not None:
            for i in range(n):
                if rr[line][i][1] == line + q:
                    rr[line][i][0] += bi
                    break
            else:
                rr[line].append([bi, line + q])
        if ci is not None:
            for i in range(n):
                if rr[line][i][1] == line - p:
                    rr[line][i][0] += ci
                    break
            else:
                rr[line].append([ci, line - p])
    return rr


def print_rare_matrix(rare, path = "aplusb - not.txt"):
    with open(path, "w") as fp:
        for i in range(len(rare)):
            for j in range(len(rare[i])):
                fp.write(f"{rare[i][j][0]}, {i}, {rare[i][j][1]}\n")


def dot_rare_with_tridiag_matrix(rare, tridiag):
    q = len(tridiag[0]) - len(tridiag[1])
    p = len(tridiag[0]) - len(tridiag[2])
    rr = [[] for i in range(len(rare))]
    for line in range(len(rare)):
        for col in range(len(rare)):
            ll = rare[line]
            a = tridiag[0][col]
            b = tridiag[1][col - q] if col >= q else None
            c = tridiag[2][col] if col < len(tridiag[2]) else None
            sumus = 0
            for ii in range(len(ll)):
                if rare[line][ii][1] == col:
                    sumus += rare[line][ii][0] * a
                if b is not None and rare[line][ii][1] == col - q:
                    sumus += rare[line][ii][0] * b
                if c is not None and rare[line][ii][1] == col + p:
                    sumus += rare[line][ii][0] * c
            if sumus != 0:
                rr[line].append([sumus, col])
    return rr


def bonus(tridiag_1, tridiag_2):
    n = len(tridiag_1[0])
    q_1 = n - len(tridiag_1[1])
    p_1 = n - len(tridiag_1[2])
    q_2 = n - len(tridiag_2[1])
    p_2 = n - len(tridiag_2[2])
    rr = [[] for i in range(n)]
    for line in range(n):
        for col in range(n):
            v_1 = {
                col: tridiag_2[0][col],
            }
            if col >= q_2:
                v_1.update({col - q_2: tridiag_2[1][col - q_2]})
            if col < len(tridiag_2[2]):
                v_1.update({col + p_2: tridiag_2[2][col]})
            v_2 = {
                line: tridiag_1[0][line]
            }
            if line < len(tridiag_1[1]):
                v_2.update({line + q_1: tridiag_1[1][line]})
            if line >= p_1:
                v_2.update({line - p_1: tridiag_1[1][line - p_1]})
            sumus = 0
            for i in v_1.keys():
                if i in v_2:
                    sumus += v_1[i] * v_2[i]
            if sumus != 0:
                rr[line].append([sumus, col])
    return rr





