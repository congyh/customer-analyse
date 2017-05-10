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

with open('../data/cleaned_test.csv', 'rt') as rf:
    rf_csv = csv.reader(rf)
    with open('../data/rfm_test.csv', 'wt') as wf:
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
            tmp_time = datetime.strptime(row[3], '%Y-%m-%d %H:%M')
            # 只记录每个顾客来说的最后一次购买时间
            if row[0] not in r_dict.keys() or tmp_time > r_dict[row[0]]:
                r_dict[row[0]] = tmp_time
        # wf_csv.writelines(r_dict)
        deadline_datetime = datetime.strptime('2010-12-10', '%Y-%m-%d')
        for key in r_dict:
            r_dict[key] = deadline_datetime - r_dict[key]
        print(r_dict)
