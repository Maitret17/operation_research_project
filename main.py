from parser import parser
from algorithm import northwest
from display import print_matrix

if __name__ == "__main__":
    n, m, cost_matrix, cost_row, provision_column = parser("1")
    print(print_matrix(n, m, cost_matrix, cost_row, provision_column))
