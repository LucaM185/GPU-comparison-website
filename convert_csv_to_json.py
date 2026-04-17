import csv
import json
import re

def extract_tflops(perf_str):
    """Extract TFLOPS value from performance string"""
    if not perf_str or perf_str.strip() == '':
        return None
    # Handle both TFLOPS and TFLOPs (capital/lowercase variations)
    match = re.search(r'([\d,]+\.?\d*)\s*(?:TFLOPS|TFLOPs|GFLOPS)', perf_str, re.IGNORECASE)
    if match:
        value = float(match.group(1).replace(',', ''))
        # Check if it's GFLOPS
        if 'GFLOPS' in perf_str.upper():
            value = value / 1000
        return value
    return None

# Read CSV and convert to JSON
gpus = []
with open('filtered_gpus.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Extract max compute performance from all available metrics
        fp32 = extract_tflops(row.get('Theoretical Performance__FP32 (float)', ''))
        fp16 = extract_tflops(row.get('Theoretical Performance__FP16 (half)', ''))
        tf32 = extract_tflops(row.get('Theoretical Performance__TF32', ''))
        bf16 = extract_tflops(row.get('Theoretical Performance__BF16', ''))
        
        all_vals = [v for v in [fp32, fp16, tf32, bf16] if v is not None]
        max_tflops = max(all_vals) if all_vals else None
        compute_str = f"{max_tflops:.3f} TFLOPS" if max_tflops else ""
        
        gpu = {
            'brand': row['Brand'],
            'name': row['Name'],
            'releaseDate': float(row['Graphics Card__Release Date']) if row['Graphics Card__Release Date'] and row['Graphics Card__Release Date'].strip() else None,
            'bandwidth': row['Memory__Bandwidth'] if row['Memory__Bandwidth'] else '',
            'compute': compute_str,
            'tensorCores': row['Render Config__Tensor Cores'] if row['Render Config__Tensor Cores'] else '',
            'memory': float(row['Memory__Memory Size']) if row['Memory__Memory Size'] and row['Memory__Memory Size'].strip() else None,
        }
        gpus.append(gpu)

# Write to JSON file
with open('gpus.json', 'w', encoding='utf-8') as f:
    json.dump(gpus, f, indent=2)

print(f"Converted {len(gpus)} GPUs to gpus.json")
