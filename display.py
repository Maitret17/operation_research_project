from utils import max_string_column, max_string_provision, max_string_label_column, INF


def print_matrix(n: int, m: int, matrix: list[list[int]], provision: list[int], cost: list[int]) -> str:  # Display the cost or transport matrix
    width = [max_string_label_column(matrix)]  # Create a width list holding the max character width for each column
    #print(cost)
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
        line = ("P" + str(i+1)).ljust(width[0])
        for j in range(m):
            line += " " + (str(matrix[i][j])).rjust(width[j+1])
        line += " " + str(provision[i]).rjust(width[-1])
        lines.append(line)

    line = "Orders".rjust(width[0])
    for j in range(m):
        line += " " + (str(cost[j])).rjust(width[j+1])
    line += " " + "".rjust(width[-1])
    lines.append(line)
    print("\n".join(lines))

def print_potential_matrix(u: list[int], v: list[int]) -> None:
    n = len(u)
    m = len(v)

    potential_matrix = [[0] * m for _ in range(n)]

    for i in range(n):
        for j in range(m):
            potential_matrix[i][j] = u[i] + v[j]

    width = [max_string_label_column(potential_matrix)]

    for j in range(m):
        max_width = len("C" + str(j + 1))
        for i in range(n):
            max_width = max(max_width, len(str(potential_matrix[i][j])))
        width.append(max_width)

    lines = []

    line = "".rjust(width[0])
    for j in range(m):
        line += " " + ("C" + str(j + 1)).rjust(width[j + 1])
    lines.append(line)

    for i in range(n):
        line = ("P" + str(i + 1)).ljust(width[0])
        for j in range(m):
            line += " " + str(potential_matrix[i][j]).rjust(width[j + 1])
        lines.append(line)

    print("\n".join(lines))


def print_marginal_matrix(marginal_matrix: list[list[int]]) -> None:
    n = len(marginal_matrix)
    m = len(marginal_matrix[0])

    width = [max_string_label_column(marginal_matrix)]

    for j in range(m):
        max_width = len("C" + str(j + 1))
        for i in range(n):
            value = marginal_matrix[i][j]
            display = "∞" if value >= INF else str(value)
            max_width = max(max_width, len(display))
        width.append(max_width)

    lines = []

    line = "".rjust(width[0])
    for j in range(m):
        line += " " + ("C" + str(j + 1)).rjust(width[j + 1])
    lines.append(line)

    for i in range(n):
        line = ("P" + str(i + 1)).ljust(width[0])
        for j in range(m):
            value = marginal_matrix[i][j]
            display = "∞" if value >= INF else str(value)
            line += " " + display.rjust(width[j + 1])
        lines.append(line)

    print("\n".join(lines))