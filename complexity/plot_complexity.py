import os
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("complexity_results.csv")
os.makedirs("complexity_plots", exist_ok=True)

time_columns = [
    ("theta_nw", "theta_NW"),
    ("theta_bh", "theta_BH"),
    ("t_nw", "t_NW"),
    ("t_bh", "t_BH"),
    ("theta_nw_plus_t_nw", "theta_NW + t_NW"),
    ("theta_bh_plus_t_bh", "theta_BH + t_BH"),
]

# Scatter plots
for column, label in time_columns:
    plt.figure()
    plt.scatter(df["n"], df[column])
    plt.xlabel("n")
    plt.ylabel("Time in seconds")
    plt.title(f"Scatter plot of {label}")
    plt.grid(True)
    plt.savefig(f"complexity_plots/scatter_{column}.png", dpi=300, bbox_inches="tight")
    plt.close()

# Worst-case curves
for column, label in time_columns:
    worst = df.groupby("n")[column].max().reset_index()

    plt.figure()
    plt.plot(worst["n"], worst[column], marker="o")
    plt.xlabel("n")
    plt.ylabel("Worst-case time (seconds)")
    plt.title(f"Worst-case curve of {label}")
    plt.grid(True)
    plt.savefig(f"complexity_plots/worst_{column}.png", dpi=300, bbox_inches="tight")
    plt.close()

# Scatter
plt.figure()
plt.scatter(df["n"], df["ratio_nw_bh"])
plt.xlabel("n")
plt.ylabel("Ratio")
plt.title("Scatter plot of (theta_NW + t_NW) / (theta_BH + t_BH)")
plt.grid(True)
plt.savefig("complexity_plots/scatter_ratio.png", dpi=300, bbox_inches="tight")
plt.close()

# Worst-case
worst_ratio = df.groupby("n")["ratio_nw_bh"].max().reset_index()

plt.figure()
plt.plot(worst_ratio["n"], worst_ratio["ratio_nw_bh"], marker="o")
plt.xlabel("n")
plt.ylabel("Worst-case ratio")
plt.title("Worst-case curve of (theta_NW + t_NW) / (theta_BH + t_BH)")
plt.grid(True)
plt.savefig("complexity_plots/worst_ratio.png", dpi=300, bbox_inches="tight")
plt.close()


print("Done. Plots are in complexity_plots/")