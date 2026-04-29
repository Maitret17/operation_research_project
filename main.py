from parser import parser
from algorithm import balashammer, northwest, acyclic, connected, fix_degeneracy, compute_potentials, marginal_cost, find_cycle, find_smallest_edge, is_optimal, apply_cycle_update, total_cost
from display import print_matrix

if __name__ == "__main__":
    n, m, cost_matrix, cost_row, provision_column = parser("7")

    matrix = northwest(n, m, cost_row, provision_column)

    print(print_matrix(n, m, matrix, provision_column, cost_row))
    print(acyclic(n, m, matrix))
    print(connected(n, m, matrix))

    print("\nAfter degeneracy fix:")

    matrix = fix_degeneracy(n, m, cost_matrix, matrix)

    print(print_matrix(n, m, matrix, provision_column, cost_row))
    print(acyclic(n, m, matrix))
    print(connected(n, m, matrix))

    print("\nPotentials:")

    u, v = compute_potentials(n, m, cost_matrix, matrix)

    print("u:", u)
    print("v:", v)

    marg = marginal_cost(n, m, u, v, cost_matrix, matrix)
    print("\nMarginal cost:")
    print(marg)

    # --- TEST ONE STEPPING-STONE UPDATE ---
    print("\nTesting stepping-stone update:")

    best_value, best_edge = find_smallest_edge(n, m, marg)

    print("Best marginal value:", best_value)
    print("Best entering edge:", best_edge)

    if is_optimal(best_value):
        print("The current proposal is optimal.")
        print("Total cost:", total_cost(cost_matrix, matrix))
    else:
        cycle = find_cycle(n, m, matrix, best_edge)
        print("Cycle:", cycle)

        print("\nBefore update:")
        print(print_matrix(n, m, matrix, provision_column, cost_row))
        print("Total cost:", total_cost(cost_matrix, matrix))

        matrix = apply_cycle_update(matrix, cycle)

        print("\nAfter update:")
        print(print_matrix(n, m, matrix, provision_column, cost_row))
        print("Total cost:", total_cost(cost_matrix, matrix))