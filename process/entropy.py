"""
计算熵

TODO 可能要用到numpy, scipy等包
"""

import numpy as np
import math

# 注意: csv文件是带头的, 第一行需要跳过. 原始数据已按照客户编号排序
r, m, f = np.loadtxt('../data/rfm_normalize.csv',
                     usecols=(1, 2, 3), delimiter=',',
                     unpack=True, skiprows=1)
# 验证了数据读取格式
print(r[0], m[0], f[0], sep=',')
# 统计客户数量
customerNums = len(r)

# 创建一个"客户数量" x "客户数量"的数组 所有的值都是随机初始化的.
entropy_matrix = np.ndarray(shape=(customerNums, customerNums),
                            dtype=float, order='F')

# 计算叉熵距离矩阵(注意不能对负数取对数)
# 基本思路为, 对每个顾客(一行)通过遍历(所有顾客)求出对其他顾客的叉熵距离, 作为矩阵中的一行
for i in range(customerNums):
    for j in range(customerNums):
        entropy_matrix[i][j] = r[i] * math.log2(r[i] / r[j]) \
                               + m[i] * math.log2(m[i] / m[j]) \
                               + f[i] * math.log2(f[i] / f[j])
# 变为对称矩阵
entropy_matrix = (entropy_matrix + entropy_matrix.T) / 2
# 验证计算结果: 是否为对称矩阵, 如果是的话, 后面两个值应该是相等的. 另外, 对角线上的值应该是0
print(entropy_matrix[0][0],
      entropy_matrix[0, customerNums - 1],
      entropy_matrix[customerNums - 1, 0], sep=',')

# TODO 计算相似度矩阵

