import csv

# Read PE data
with open('ETFData/hs300_PE-TTM.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    pe_data = []
    for i, row in enumerate(reader):
        # Check headers on first row
        if i == 0:
            print('Headers:', list(row.keys()))
        # Look for PE column
        pe_val = row.get('PE-TTM市值加权') or row.get('PE-TTM')
        if pe_val:
            pe = float(pe_val.replace('=', ''))
            pe_data.append({'date': row.get('日期'), 'pe': pe})
        if i > 4870:  # Limit to avoid too much output
            break

# Sort PE values for percentile calculation
pe_values = sorted([d['pe'] for d in pe_data])
total = len(pe_values)

print(f'Total PE records: {total}')
print(f'Min PE: {pe_values[0]:.4f}')
print(f'Max PE: {pe_values[-1]:.4f}')

# Calculate percentile for 2025-12-19 (PE = 13.9633)
target_pe = 13.9633
lower_count = sum(1 for v in pe_values if v <= target_pe)
percentile = ((lower_count - 1) / (total - 1)) * 100

print(f'PE {target_pe} percentile: {percentile:.2f}%')
print(f'CSV value for 2025-12-19: 61.84%')
