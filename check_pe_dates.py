import csv

# 读取 PE 数据，找最早日期
with open('ETFData/hs300_PE-TTM.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    dates = []
    for i, row in enumerate(reader):
        date = row.get('日期', '').strip()
        if date and date != '数据来源于' and len(date) == 10:  # 排除非日期行，日期应该是 YYYY-MM-DD 格式
            dates.append(date)
    
    dates.sort()
    print(f'最早日期: {dates[0]}')
    print(f'最晚日期: {dates[-1]}')
    print(f'总记录数: {len(dates)}')
    
    # 检查 2010-11-09 是否存在
    if '2010-11-09' in dates:
        print('2010-11-09 存在于 PE 数据中')
    else:
        print('2010-11-09 不存在于 PE 数据中')
