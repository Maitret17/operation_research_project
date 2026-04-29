def max_string_column(column_index: int, matrix: list[list[int]], cost: list[int]) -> int:  # Return the max character size in the j column
    lst = []
    for i in range(len(matrix)):
        lst.append(len(str(matrix[i][column_index])))
    #print(matrix)
    #print(column_index)
    #print(cost)
    lst.append(len(str(cost[column_index])))
    return max(lst)


def max_string_provision(provision: list[int]) -> int:  # Return the max character size in the provision column
    lst = [len("Provisions")]
    for p in provision:
        lst.append(len(str(p)))
    return max(lst)


def max_string_label_column(matrix: list[list[int]]) -> int:  # Return the max character size in the label column
    lst = [len("Orders")]
    for j in range(len(matrix[0])):
        lst.append(len(f"C{j+1}"))
    return max(lst)

def count_basic_edges(transport_matrix: list[list[int]]) -> int:
    count = 0
    for row in transport_matrix:
        for value in row:
            if value != 0:
                count += 1
    return count


def is_degenerate(n: int, m: int, transport_matrix: list[list[int]]) -> bool:
    return count_basic_edges(transport_matrix) < n + m - 1


