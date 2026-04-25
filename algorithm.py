def northwest(n: int, m: int, cost_row: list[int], provision_column: list[int]) -> list[list[int]]:
    transport_matrix = [[0] * m for i in range(n)]
    i, j = 0, 0
    temp_cost_row, temp_provision_column = list(cost_row), list(provision_column)

    while i < n and j < m:
        allocation = min(temp_provision_column[i], temp_cost_row[j])
        transport_matrix[i][j] = allocation
        temp_provision_column[i] -= allocation
        temp_cost_row[j] -= allocation
        if temp_provision_column[i] == 0:
            i += 1
        if temp_cost_row[j] == 0:
            j += 1

    return transport_matrix


def total_cost(cost_matrix: list[list[int]], transport_matrix: list[list[int]]) -> int: # Takes the transport matrix and its cost_matrix to find the total cost of the proposed transport solution
    total = 0
    for i in range(len(cost_matrix)):
        for j in range(len(cost_matrix[0])):
            total += cost_matrix[i][j] * transport_matrix[i][j]
    return total
