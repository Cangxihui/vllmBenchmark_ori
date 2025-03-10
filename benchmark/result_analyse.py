import json

# 打开并读取 JSON 文件
filepath = r'C:\Users\Administrator.SY-202403121806\Desktop\result\vllm_infqps_DeepSeek-R1_V0-FLASHMLA.json'
with open(filepath, 'r', encoding='utf-8') as file:
    data = json.load(file)  # 解析 JSON 数据

print(type(data))
# 如果 JSON 文件中的数据是一个字典，你可以遍历其中的键值对
if isinstance(data, dict):
    for key, value in data.items():
        print(f"{key}")

print('=========================================')


print(data.get("mean_ttft_ms"))
# 提取基本信息
basic_info = {
    "date": data.get("date"),
    "backend": data.get("backend"),
    "model_id": data.get("model_id"),
    "num_prompts": data.get("num_prompts"),
    "duration_seconds": data.get("duration"),
    "total_input_tokens": data.get("total_input_tokens"),
    "total_output_tokens": data.get("total_output_tokens")
}

# 提取性能指标
performance_metrics = {
    "request_throughput": data.get("request_throughput"),
    "output_throughput": data.get("output_throughput"),
    "total_token_throughput": data.get("total_token_throughput"),
    # 注意字段名可能有拼写错误
    "request_goodput": data.get("request_goodput:")  # 原数据中键名带冒号
}

# 提取时间相关数据
timing_data = {
    "ttfts_avg": sum(data["ttfts"]) / len(data["ttfts"]) if data.get("ttfts") else 0,
    "input_lens_stats": {
        "avg": sum(data["input_lens"]) / len(data["input_lens"]),
        "max": max(data["input_lens"]),
        "min": min(data["input_lens"])
    }
}

# 打印结果
print("Basic Information:")
for key, value in basic_info.items():
    print(f"{key:20}: {value}")

print("\nPerformance Metrics:")
for key, value in performance_metrics.items():
    print(f"{key:25}: {value}")

print("\nTiming Analysis:")
print(f"{'Average TTFT':25}: {timing_data['ttfts_avg']:.2f} seconds")
print(f"{'Avg Input Length':25}: {timing_data['input_lens_stats']['avg']}")
print(f"{'Max Input Length':25}: {timing_data['input_lens_stats']['max']}")

# 输出示例：
# Basic Information:
# date                : 20250309-043445
# backend             : vllm
# model_id            : deepseek-ai/DeepSeek-R1
# num_prompts         : 100
# duration_seconds    : 324.7881739280001
# total_input_tokens  : 3000000
# total_output_tokens : 10000

# Performance Metrics:
# request_throughput       : 0.3078929838811442
# output_throughput        : 30.78929838811442
# total_token_throughput   : 9267.57881482244
# request_goodput          : None

# Timing Analysis:
# Average TTFT             : 142.07 seconds
# Avg Input Length         : 30000.0
# Max Input Length         : 30000