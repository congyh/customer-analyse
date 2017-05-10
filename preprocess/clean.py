"""
读入原始数据, 对数据进行清洗

完成了以下任务:
1. 去除了没有customerId的字段.
2. 去除了缺失信息或者混乱的字段.
"""
import csv
from collections import namedtuple

count_for_not_valid = 0

with open('../data/工作簿1.csv', 'rt') as rf:
    rf_csv = csv.reader(rf)
    # Row = namedtuple('Row', headings)
    with open('../data/cleaned.csv', 'wt') as wf:
        wf_csv = csv.writer(wf)
        headings = next(rf_csv)
        wf_csv.writerow(headings)
        for row in rf_csv:
            # row = Row(*r)
            # if len(row) == 4:
            #     wf_csv.writerow(row)
            valid = True
            for entry in row[0:2]:
                if not entry[1:].isnumeric():
                    valid = False
                    count_for_not_valid = count_for_not_valid + 1
                    break
            if valid:
                wf_csv.writerow(row)


print('不合格的条目: ', count_for_not_valid)
print('clean finished.')

