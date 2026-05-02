from parser import parser
from algorithm import balashammer, northwest, acyclic, connected, fix_degeneracy, total_cost, compute_potentials, marginal_cost, find_smallest_edge, find_cycle, is_optimal, apply_cycle_update
from display import print_matrix, print_potential_matrix, print_marginal_matrix
from utils import count_basic_edges, is_degenerate, clean_epsilon
import os


def sort_key(x):
    try:
        return (0, int(x))
    except ValueError:
        return (1, str(x))


def stepping_stone(n, m, cost_matrix, transport_matrix, provision_column, cost_row):  # The wrapper function
    iteration = 1

    while True:
        print(f"----Iteration {iteration}----\n")
        print("Current transportation proposal:")
        print_matrix(n, m, transport_matrix, provision_column, cost_row)
        print(f"\nCurrent total cost: {total_cost(cost_matrix, transport_matrix)}")

        print("Degeneracy test:")
        print(f"Basic edges: {count_basic_edges(transport_matrix)}")
        print(f"Expected basic edges: {n + m - 1}\n")

        if is_degenerate(n, m, transport_matrix):
            print("The proposal is degenerate")
            transport_matrix = fix_degeneracy(n, m, cost_matrix, transport_matrix)
            print("Proposal after degeneracy fix:")
            print_matrix(n, m, transport_matrix, provision_column, cost_row)
            # Maybe show it after fixed
        else:
            print("The proposal is not degenerate")

        print("\nTransport graph test:")

        connected(n, m, transport_matrix)
        print("The graph is acyclic") if acyclic(n, m, transport_matrix) else print("The graph isn't acyclic")
        if connected and acyclic:
            print("The transport graph is a tree")
        else:
            print("The transport graph is not a tree")

        u, v = compute_potentials(n, m, cost_matrix, transport_matrix)
        print("\nPotential matrix:")
        print_potential_matrix(u, v)

        marginal_matrix = marginal_cost(n, m, u, v, cost_matrix, transport_matrix)
        print("\nMarginal cost matrix:")
        print_marginal_matrix(marginal_matrix)

        best_value, best_edge = find_smallest_edge(n, m, marginal_matrix)

        if is_optimal(best_value):
            print("\nThe proposal is optimal")
            break

        print(f"\nEdge to add: row {best_edge[0] + 1}, column {best_edge[1] + 1}")
        print(f"Marginal cost: {best_value}")

        transport_matrix[best_edge[0]][best_edge[1]] = -1

        cycle = find_cycle(n, m, transport_matrix, best_edge)
        print("Cycle: ")
        print(cycle)

        transport_matrix = apply_cycle_update(transport_matrix, cycle)

        print("\nUpdated transportation proposal:")
        print_matrix(n, m, transport_matrix, provision_column, cost_row)
        print("")
        iteration += 1

    transport_matrix = clean_epsilon(transport_matrix)
    print("Minimal transportation proposal:")
    print_matrix(n, m, transport_matrix, provision_column, cost_row)
    print(f"\nMinimal cost: {total_cost(cost_matrix, transport_matrix)}")
    return transport_matrix


def menu():

    while True:
        print("transportation problems file list:")
        transp_list = os.listdir("data/")
        for filename in transp_list:
            if filename.endswith(".txt"):
                name = filename[:-4]
                transp_list[transp_list.index(filename)] = name
            else:
                transp_list.remove(filename)

        transp_list = sorted(transp_list, key=sort_key)

        for filename in transp_list:
            print(filename)
        print("="*80)
        print("Select a transportation problem file or type 'q' to exit :")
        transp_selected = input()
        while not (transp_selected in transp_list):
            if transp_selected.lower() == "q":
                print("Goodbye")
                return
            print("The transportation problem file's name is incorrect")
            print("Select a transportation problem file or type 'q' to exit :")
            transp_selected = input()

        print("="*80)
        n, m, cost_matrix, cost_row, provision_column = parser(transp_selected)
        print("The cost matrix:")
        # Display corresponding matrix
        print_matrix(n, m, cost_matrix, provision_column, cost_row)

        print("=" * 80)
        print(
            "Select which algorithm to use:\n"
            "1 - northwest\n"
            "2 - balashammer"
        )

        algo_selected = input()

        while algo_selected not in ["1", "2"]:
            print("Incorrect algorithm choice")
            print(
                "Select which algorithm to use:\n"
                "1 - northwest\n"
                "2 - balashammer"
            )
            algo_selected = input()

        print("=" * 80)
        if algo_selected == "1":
            transp_matrix = northwest(n, m, cost_row, provision_column)
        if algo_selected == "2":
            transp_matrix = balashammer(n, m, cost_matrix, cost_row, provision_column)

        if transp_matrix is not None: # I'm unsure whether we keep this or not. It's not really asked for
            print("The initial transportation proposal: ")
            print_matrix(n, m, transp_matrix, provision_column, cost_row)
            print("")
            print(f"Total transport cost: {total_cost(cost_matrix, transp_matrix)}")
            print("")
            transp_matrix = stepping_stone(n, m, cost_matrix, transp_matrix, provision_column, cost_row)
        print("="*80)


if __name__ == "__main__":
    menu()
