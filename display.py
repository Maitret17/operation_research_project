from utils import max_string_column, max_string_provision, max_string_label_column


def print_matrix(n: int, m: int, matrix: list[list[int]], provision: list[int], cost: list[int]) -> str:  # Display the cost or transport matrix
    width = [max_string_label_column(matrix)]  # Create a width list holding the max character width for each column
    print(cost)
    for j in range(m):
        width.append(max_string_column(j, matrix, cost))
    width.append(max_string_provision(provision))

    lines = []
    line = "".rjust(width[0])  # rjust right-aligns the content of the string, to avoid shifting columns
    for j in range(m):
        line += " " + ("C" + str(j+1)).rjust(width[j+1])
    line += " " + "Provisions".rjust(width[-1])
    lines.append(line)

    for i in range(n):
        line = ("P" + str(i+1)).rjust(width[0])
        for j in range(m):
            line += " " + (str(matrix[i][j])).rjust(width[j+1])
        line += " " + str(provision[i]).rjust(width[-1])
        lines.append(line)

    line = "Orders".rjust(width[0])
    for j in range(m):
        line += " " + (str(cost[j])).rjust(width[j+1])
    line += " " + "".rjust(width[-1])
    lines.append(line)
    return "\n".join(lines)


