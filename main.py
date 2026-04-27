from parser import parser
from algorithm import balashammer, northwest, acyclic
from display import print_matrix

if __name__ == "__main__":
    n, m, cost_matrix, cost_row, provision_column = parser("10")
    print(northwest(n,m,cost_row,provision_column))
    print(acyclic(n, m, northwest(n,m,cost_row,provision_column)))
    print("\n")
    print(balashammer(n,m,cost_matrix,cost_row,provision_column))
    print(acyclic(n, m, balashammer(n,m,cost_matrix,cost_row,provision_column)))
    print("\n")
    print(print_matrix(n, m, cost_matrix, provision_column, cost_row))  
