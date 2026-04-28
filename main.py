from parser import parser
from algorithm import balashammer, northwest, acyclic, connected, fix_degeneracy
from display import print_matrix

if __name__ == "__main__":
    n, m, cost_matrix, cost_row, provision_column = parser("1")

    matrix = northwest(n, m, cost_row, provision_column)
    print(print_matrix(n, m, matrix, provision_column, cost_row))
    print(acyclic(n, m, matrix))
    print(connected(n, m, matrix))

    print("\n")

    matrix = fix_degeneracy(n, m, cost_matrix, matrix)
    print(print_matrix(n, m, matrix, provision_column, cost_row))
    print(acyclic(n, m, matrix))
    print(connected(n, m, matrix))