import csv

# 加载基金数据
fundData = []
with open('ETFData/易方达沪深300ETF联接A_基金净值.csv', 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        line = line.strip()
        if not line or i == 0:  # 跳过空行和标题行
            continue
        parts = line.split(',')
        if len(parts) >= 2 and parts[0].strip():
            date = parts[0].strip()
            try:
                value = float(parts[1].strip().replace('=', ''))
                if 0.5 < value < 3.5:  # 有效的基金净值范围
                    fundData.append({'date': date, 'close': value})
            except:
                pass

print(f'基金数据: {len(fundData)} 条记录')
if fundData:
    print(f'  最早: {fundData[-1]["date"]}')
    print(f'  最晚: {fundData[0]["date"]}')

# 加载指数数据
indexData = []
with open('ETFData/hs300_base_data.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            indexData.append({'date': row['date'].strip(), 'close': float(row['close'].strip())})
        except:
            pass

print(f'指数数据: {len(indexData)} 条记录')
if indexData:
    indexData_sorted = sorted(indexData, key=lambda x: x['date'])
    print(f'  最早: {indexData_sorted[0]["date"]}')
    print(f'  最晚: {indexData_sorted[-1]["date"]}')

# 加载PE数据
peData = []
with open('ETFData/hs300_PE-TTM.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        try:
            date = row.get('日期', '').strip()
            pe_str = row.get('PE-TTM市值加权', '').strip().replace('=', '')
            percentile_str = row.get('PE-TTM 分位点', '').strip().replace('=', '')
            
            if date and pe_str and percentile_str:
                pe = float(pe_str)
                percentile = float(percentile_str) * 100
                if 5 < pe < 100:  # 有效的PE值范围
                    peData.append({'date': date, 'pe': pe, 'percentile': percentile})
        except Exception as e:
            if not peData:  # 只打印前几个错误
                print(f'PE数据错误: {row}, 错误: {e}')

print(f'PE数据: {len(peData)} 条记录')
if peData:
    peData_sorted = sorted(peData, key=lambda x: x['date'])
    print(f'  最早: {peData_sorted[0]["date"]}')
    print(f'  最晚: {peData_sorted[-1]["date"]}')
else:
    # 调试：看看是否能读出数据
    with open('ETFData/hs300_PE-TTM.csv', 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        print('PE CSV 列名:', list(reader.fieldnames))
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i < 3:
                print(f'Row {i}: 日期={row.get("日期")}, PE={row.get("PE-TTM市值加权")}, 分位点={row.get("PE-TTM 分位点")}')
            if i >= 2:
                break

# 检查 2010-11-09 是否在各个数据源中
test_date = '2010-11-09'
fund_has = any(d['date'] == test_date for d in fundData)
index_has = any(d['date'] == test_date for d in indexData)
pe_has = any(d['date'] == test_date for d in peData)

print(f'\n检查日期 {test_date}:')
print(f'  基金: {fund_has}')
print(f'  指数: {index_has}')
print(f'  PE: {pe_has}')

# 合并数据（按照HTML逻辑）
mergedData = []
for indexItem in indexData:
    peItem = next((p for p in peData if p['date'] == indexItem['date']), None)
    fundItem = next((f for f in fundData if f['date'] == indexItem['date']), None)
    
    if peItem and fundItem:
        mergedData.append({
            'date': indexItem['date'],
            'close': indexItem['close'],
            'pe': peItem['pe'],
            'percentile': peItem['percentile'],
            'fundClose': fundItem['close']
        })

print(f'\n合并数据: {len(mergedData)} 条记录')
if mergedData:
    mergedData_sorted = sorted(mergedData, key=lambda x: x['date'])
    print(f'  最早: {mergedData_sorted[0]["date"]}')
    print(f'  最晚: {mergedData_sorted[-1]["date"]}')
    
    # 检查 2010-11-09 是否在合并数据中
    merged_has = any(d['date'] == test_date for d in mergedData)
    print(f'  {test_date} 在合并数据中: {merged_has}')
