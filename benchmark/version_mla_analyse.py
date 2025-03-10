import json
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# file_path
folder_path = Path(r'C:\Users\Administrator.SY-202403121806\Desktop\result')
result_dir = r'../result/'
## fix suffixed
suffixes = ["V0-FLASHMLA.json", "V0-TRITONMLA.json", "V1-FLASHMLA.json", "V1-TRITONMLA.json"]

output_throughput_values = []
mean_ttfts_value = []
labels = []

# search in dir
for file_path in folder_path.glob("*.json"):
    if any(file_path.name.endswith(suffix) for suffix in suffixes):
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
            output_throughput = data.get("output_throughput", 0)  #  output_throughput
            mean_ttft = data.get("mean_ttft_ms", 0)
            labels.append(str(file_path.stem).split('_')[-1])  # remove ".json"
            output_throughput_values.append(output_throughput)
            mean_ttfts_value.append(mean_ttft)
# Seaborn  Nature Style
sns.set_theme(style="whitegrid", font="Times New Roman", font_scale=1.5)

labels = [label.replace("MLA", "") for label in labels]



# Output_throughput
fig, ax = plt.subplots(figsize=(8, 6), dpi=300)
colors = sns.color_palette("pastel")
# bar
x_positions = range(len(labels))
ax.bar(labels, output_throughput_values, color=colors, edgecolor="black", linewidth=2)


# 设置 X 轴刻度和标签
ax.set_xticks(x_positions)
ax.set_xticklabels(labels, fontsize=12, ha="center")
ax.set_xlabel("Model Version", fontsize=16, fontweight="bold")
ax.set_ylabel("Output Throughput", fontsize=16, fontweight="bold")
ax.set_title("Output Throughput Comparison", fontsize=18, fontweight="bold", pad=15)

# remove border
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# modify X
# ax.set_xticklabels(labels, ha="right")


# save figure
plt.tight_layout()
output_filename = result_dir + "vLLMVersion_MLA_outthr.png"
plt.savefig(output_filename, dpi=300)  # 600 DPI

print(f"Saved figure to {output_filename}")


# Mean_ttft
fig2, ax2 = plt.subplots(figsize=(8, 6), dpi=300)
colors2 = sns.color_palette("pastel")
# bar
ax2.bar(labels, mean_ttfts_value, color=colors2, edgecolor="black", linewidth=2)

ax2.set_xticks(x_positions)
ax2.set_xticklabels(labels, fontsize=12, ha="center")

ax2.set_xlabel("Model Version", fontsize=16, fontweight="bold")
ax2.set_ylabel("TTFT/ms", fontsize=16, fontweight="bold")
ax2.set_title("Mean TTFT Comparison", fontsize=18, fontweight="bold", pad=15)

# remove border
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)

# modify X
# ax2.set_xticklabels(labels, fontsize=12,  ha="right")

# save figure
plt.tight_layout()
output_filename2 = result_dir + "Mean_ttft_compare.png"
plt.savefig(output_filename2, dpi=600)  # 600 DPI

print(f"Saved figure to {output_filename2}")



