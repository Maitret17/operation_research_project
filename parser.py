def parser(num_file):
    with open(f"data/{num_file}.txt", "r") as f:
        n, m = map(int, f.readline().split())
        cost_matrix = []
        provision_column = []
        for i in range(n):
            line = list(map(int, f.readline().split()))
            cost_matrix.append(line[:m])
            provision_column.append(line[m:][0])
        cost_row = list(map(int, f.readline().split()))

        return n, m, cost_matrix, cost_row, provision_column
