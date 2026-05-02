import csv
import random
import time
import os
from copy import deepcopy
from contextlib import redirect_stdout

from algorithm import northwest, balashammer
from main import stepping_stone


def generate_problem(n: int):
    cost_matrix = [[random.randint(1, 100) for _ in range(n)] for _ in range(n)]
    temp_matrix = [[random.randint(1, 100) for _ in range(n)] for _ in range(n)]

    provision_column = [sum(temp_matrix[i][j] for j in range(n)) for i in range(n)]
    cost_row = [sum(temp_matrix[i][j] for i in range(n)) for j in range(n)]

    return cost_matrix, cost_row, provision_column


def measure_once(n: int):
    cost_matrix, cost_row, provision_column = generate_problem(n)

    start = time.perf_counter()
    nw_matrix = northwest(n, n, cost_row, provision_column)
    theta_nw = time.perf_counter() - start

    start = time.perf_counter()
    bh_matrix = balashammer(n, n, cost_matrix, cost_row, provision_column)
    theta_bh = time.perf_counter() - start

    with open(os.devnull, "w", encoding="utf-8") as devnull:
        start = time.perf_counter()
        with redirect_stdout(devnull):
            stepping_stone(n, n, cost_matrix, deepcopy(nw_matrix), provision_column, cost_row)
        t_nw = time.perf_counter() - start

        start = time.perf_counter()
        with redirect_stdout(devnull):
            stepping_stone(n, n, cost_matrix, deepcopy(bh_matrix), provision_column, cost_row)
        t_bh = time.perf_counter() - start

    return theta_nw, theta_bh, t_nw, t_bh


def main():
    sizes = [10, 40, 100]
    repetitions = 100

    with open("complexity_results.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "n",
            "run",
            "theta_nw",
            "theta_bh",
            "t_nw",
            "t_bh",
            "theta_nw_plus_t_nw",
            "theta_bh_plus_t_bh",
            "ratio_nw_bh"
        ])

        for n in sizes:
            for run in range(1, repetitions + 1):
                print(f"n={n}, run={run}/{repetitions}")

                theta_nw, theta_bh, t_nw, t_bh = measure_once(n)

                total_nw = theta_nw + t_nw
                total_bh = theta_bh + t_bh
                ratio = total_nw / total_bh if total_bh != 0 else ""

                writer.writerow([
                    n,
                    run,
                    theta_nw,
                    theta_bh,
                    t_nw,
                    t_bh,
                    total_nw,
                    total_bh,
                    ratio
                ])

                file.flush()


if __name__ == "__main__":
    main()