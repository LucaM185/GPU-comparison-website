# load gpus.csv
import pandas as pd
df = pd.read_csv('gpus.csv')

# print the titles
print(df.columns.tolist())

# List relevant columns
relevant_columns = ['Brand', 'Name', 'Graphics Card__Release Date', 'Memory__Bandwidth', 'Theoretical Performance__FP32 (float)', 'Theoretical Performance__FP16 (half)', 'Theoretical Performance__TF32', 'Theoretical Performance__BF16', 'Render Config__Tensor Cores', 'Memory__Memory Size']
df_relevant = df[relevant_columns]


# filter only ones with at least 2 GB ram
# Convert memory size to numeric (in GB)
def convert_to_gb(memory_str):
	import re
	match = re.search(r'(\d+)\s*(KB|MB|GB)', str(memory_str))
	if match:
		value, unit = float(match.group(1)), match.group(2)
		if unit == 'KB':
			return value / (1024 * 1024)
		elif unit == 'MB':
			return value / 1024
		else:  # GB
			return value
	return None

df_relevant['Memory__Memory Size'] = df_relevant['Memory__Memory Size'].apply(convert_to_gb)
df_filtered = df_relevant[df_relevant['Memory__Memory Size'] >= 4]

print(df_filtered)

# export this to a new csv
# Parse dates - handle mixed formats (dates with ordinal suffixes, or just years)
def parse_release_date(date_str):
	import re
	if pd.isna(date_str):
		return None
	date_str = str(date_str).strip()
	# Remove ordinal suffixes (st, nd, rd, th)
	cleaned = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str)
	try:
		return pd.to_datetime(cleaned).year
	except:
		return None

df_filtered['Graphics Card__Release Date'] = df_filtered['Graphics Card__Release Date'].apply(parse_release_date)
df_filtered.to_csv('filtered_gpus.csv', index=False)