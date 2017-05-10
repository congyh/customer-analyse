"""
RFM值计算

思路:
实际上就是几个简单的for循环处理
步骤:
1. 字符串->日期, 然后进行计算
2. 需要用一种数据结构来保存每个顾客的结果
"""
import csv
from datetime import datetime

with open('../data/cleaned.csv', 'rt') as rf:
    rf_csv = csv.reader(rf)
    with open('../data/rfm.csv', 'wt') as wf:
        wf_csv = csv.writer(wf)
        deprecated_headings = next(rf_csv)
        # TODO 下面还没想好, 可能需要改变头
        headings = ['customerId', 'R', 'F', 'M']
        wf_csv.writerow(headings)
        r_dict = {}
        for row in rf_csv:
            # 到这里读完了所有行, 并且转变为一个list了.
            # TODO 或许保存为一个dict要更加容易{'customerId': '记录list'}
            # TODO 这里要对RMF值进行计算
            # 1. 排序:
            # R值计算的时候只需要取最后一个购买日期字段就可以了.
            if datetime(row[3]) > r_dict[row[0]]:
                r_dict[row[0]] = datetime(row[3])
