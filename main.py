from parser import parser
from algorithm import balashammer, northwest
from display import print_matrix

if __name__ == "__main__":
    n, m, cost_matrix, cost_row, provision_column = parser("6")
    print(northwest(n,m,cost_row,provision_column))
    print(balashammer(n,m,cost_matrix,cost_row,provision_column))

    print(print_matrix(n, m, cost_matrix, provision_column, cost_row))

