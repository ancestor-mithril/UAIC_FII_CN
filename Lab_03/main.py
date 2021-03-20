from functions import read_rare_matrix, read_tridiagonal_matrix, sum_rare_with_tridiag_matrix, print_rare_matrix, \
    dot_rare_with_tridiag_matrix, bonus


def run():
    # rare_matrix = read_rare_matrix()
    # tridiagonal_matrix = read_tridiagonal_matrix()
    # print(rare_matrix)
    # print(tridiagonal_matrix[0])
    # print(tridiagonal_matrix[1])
    # print(tridiagonal_matrix[2])
    # sum = sum_rare_with_tridiag_matrix(rare_matrix, tridiagonal_matrix)
    # print_rare_matrix(sum)
    # print_rare_matrix(read_rare_matrix("aplusb.txt"), "aplusb - ei.txt")
    # prod = dot_rare_with_tridiag_matrix(rare_matrix, tridiagonal_matrix)
    # print_rare_matrix(prod, "aorib - noi.txt")
    # print_rare_matrix(read_rare_matrix("aorib.txt"), "aorib - ei.txt")
    tri_1 = read_tridiagonal_matrix("c.txt")
    tri_2 = read_tridiagonal_matrix("c.txt")
    prod = bonus(tri_1, tri_2)
    print_rare_matrix(prod, "bonus.txt")


if __name__ == '__main__':
    run()
