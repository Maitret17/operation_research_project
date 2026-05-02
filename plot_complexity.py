import os
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("complexity_results.csv")
os.makedirs("complexity_plots", exist_ok=True)

columns = [
    ("theta_nw", "theta_NW"),
    ("theta_bh", "theta_BH"),
    ("t_nw", "t_NW"),
    ("t_bh", "t_BH"),
    ("theta_nw_plus_t_nw", "theta_NW + t_NW"),
    ("theta_bh_plus_t_bh", "theta_BH + t_BH"),
    ("ratio_nw_bh", "(theta_NW + t_NW) / (theta_BH + t_BH)")
]

for column, label in columns:
    plt.figure()
    plt.scatter(df["n"], df[column])
    plt.xlabel("n")
    plt.ylabel("Time in seconds" if column != "ratio_nw_bh" else "Ratio")
    plt.title(f"Scatter plot of {label}")
    plt.grid(True)
    plt.savefig(f"complexity_plots/scatter_{column}.png", dpi=300, bbox_inches="tight")
    plt.close()

for column, label in columns:
    worst = df.groupby("n")[column].max().reset_index()

    plt.figure()
    plt.plot(worst["n"], worst[column], marker="o")
    plt.xlabel("n")
    plt.ylabel("Worst value")
    plt.title(f"Worst-case curve of {label}")
    plt.grid(True)
    plt.savefig(f"complexity_plots/worst_{column}.png", dpi=300, bbox_inches="tight")
    plt.close()

print("Done. Plots are in complexity_plots/")