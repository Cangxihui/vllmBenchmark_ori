import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import re

# Set Seaborn style for academic papers
sns.set_style("whitegrid")
sns.set_context("paper", font_scale=1.5)


# Function to parse CSV files and compute throughput and TFTT
def parse_files(file_pattern):
    results = {}
    files = glob.glob(file_pattern)

    for file in files:
        df = pd.read_csv(file)

        # Extract hist, ans, and qps values from filename
        match = re.search(r'hist(\d+)_ans(\d+)_qps(\d+)', file)
        if not match:
            continue

        hist_value, ans_value, qps_value = map(int, match.groups())
        key = f"hist{hist_value}_ans{ans_value}"

        throughput = np.mean(df["generation_tokens"] / df["generation_time"])
        tftt = np.mean(df["ttft"])

        if key not in results:
            results[key] = {"qps": [], "throughput": [], "tftt": []}

        results[key]["qps"].append(qps_value)
        results[key]["throughput"].append(throughput)
        results[key]["tftt"].append(tftt)

    # Sort data by QPS for smooth line plots
    for key in results:
        sorted_indices = np.argsort(results[key]["qps"])
        results[key]["qps"] = np.array(results[key]["qps"])[sorted_indices]
        results[key]["throughput"] = np.array(results[key]["throughput"])[sorted_indices]
        results[key]["tftt"] = np.array(results[key]["tftt"])[sorted_indices]

    return results


# Load data
data = parse_files("C:/Users/Administrator.SY-202403121806/Desktop/deepseek_distill_sglang_0312/20250302_hist*_ans*_qps*.csv")

# Define plot colors for different categories
plot_colors = {
    "hist2000_ans100": "blue",
    "hist2000_ans2000": "green",
    "hist29000_ans100": "red"
}

# Plot Throughput vs QPS
plt.figure(figsize=(8, 6))
for key, color in plot_colors.items():
    if key in data:
        plt.plot(data[key]["qps"], data[key]["throughput"], marker='o', linestyle='-', color=color, label=key)

plt.xlabel("QPS")
plt.ylabel("Throughput (tokens/s)")
plt.title("Throughput vs QPS")
plt.legend()
plt.grid(True, linestyle="--", linewidth=0.5)
plt.savefig("Sglang-throughput_vs_qps.png", dpi=300, bbox_inches='tight')
plt.show()

# Plot TFTT vs QPS
plt.figure(figsize=(8, 6))
for key, color in plot_colors.items():
    if key in data:
        plt.plot(data[key]["qps"], data[key]["tftt"], marker='s', linestyle='-', color=color, label=key)

plt.xlabel("QPS")
plt.ylabel("TFTT (s)")
plt.title("TFTT vs QPS")
plt.legend()
plt.grid(True, linestyle="--", linewidth=0.5)
plt.savefig("Sglang-tftt_vs_qps.png", dpi=300, bbox_inches='tight')
plt.show()
