"""
计算熵
"""

import numpy as np
import math
import csv

# 注意: csv文件是带头的, 第一行需要跳过. 原始数据已按照客户编号排序
customerId, r, m, f = np.loadtxt('../data/rfm_normalize.csv',
                                 delimiter=',',
                                 unpack=True, skiprows=1)
# 验证了数据读取格式
print('=========== 验证数据读取格式 ===============')
print('r:', r[0], 'f:', f[0], 'm:', m[0], sep=' ')
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
print('=========== 验证叉熵矩阵计算结果 ===============')
print('某对角线元素:', entropy_matrix[0][0],
      '对称矩阵元素1:', entropy_matrix[0, customerNums - 1],
      '对称矩阵元素2:', entropy_matrix[customerNums - 1, 0], sep=' ')

# 持久化entropy_matrix
np.savetxt('../data/entropy_matrix.csv', entropy_matrix, delimiter=',')

# 创建相似度矩阵
similarity_matrix = np.ndarray(shape=(customerNums, customerNums),
                               dtype=float, order='F')
# entropy_matrix矩阵平均值计算
entropy_avg = np.mean(entropy_matrix)
print('entropy_avg:', entropy_avg)

# alpha计算
alpha = -math.log(0.5, math.e) / entropy_avg
print('alpha:', alpha)
# 计算相似度矩阵
for i in range(customerNums):
    for j in range(customerNums):
        similarity_matrix[i][j] = math.pow(math.e, -alpha * entropy_matrix[i][j])

# 相似度矩阵按行求和, 是一个(customerNum, 1)维的数组
# similarity_matrix_row_sum = row_sum = np.sum(similarity_matrix, axis=0)

# 相似度矩阵归一化
# for i in range(customerNums):
#     for j in range(customerNums):
#         # 归一化
#         similarity_matrix[i][j] = similarity_matrix[i][j] / row_sum[i]

# 持久化similarity_matrix
np.savetxt('../data/similarity_matrix.csv', similarity_matrix, delimiter=',')

# 创建顾客熵值数组
entropy_list = np.ndarray(shape=(customerNums,), dtype=float, order='F')

# 计算顾客熵值
for i in range(customerNums):
    entropy_list[i] = 0
    for j in range(customerNums):
        # 跳过相似度为1的入口
        if j != i and similarity_matrix[i][j] != 1:
            entropy_list[i] += similarity_matrix[i][j] * math.log2(similarity_matrix[i][j]) \
                               + (1 - similarity_matrix[i][j]) * math.log2(1 - similarity_matrix[i][j])
    # 取反, 保留4位小数
    entropy_list[i] = round(-entropy_list[i], 4)

# 持久化熵值
# np.savetxt('../data/entropy.csv', entropy_list)

# 持久化熵值最终结果
for i in range(len(customerId)):
    customerId[i] = int(customerId[i])
entropy = zip(customerId, entropy_list)
entropy = list(entropy)
with open('../data/entropy.csv', 'wt') as wf:
    wf_csv = csv.writer(wf)
    headings = ['customerId', 'entropy']
    wf_csv.writerow(headings)
    for row in entropy:
        wf_csv.writerow(row)

# 聚类中心计算

# 按照熵值排序(按照熵值字段排序)
# entropy_sorted = sorted(entropy, key=lambda item: item[1])

# 保存聚类中心结果
cluster_center = []

while True:
    # 求当前entropy的最小值对应的tuple(customerId, entropy)
    entropy_min = min(entropy, key=lambda item: item[1])
    # 说明聚类中心已经查找完毕, 将退出循环
    if entropy_min[1] == 10000:
        break
    cluster_center.append(entropy_min)
    # 获取index
    entropy_min_index = entropy.index(entropy_min)
    entropy[entropy_min_index] = (None, 10000)
    for j in range(customerNums):
        if j != entropy_min_index and similarity_matrix[entropy_min_index][j] > 0.75:
            # 效果相当于将这一个相似的顾客剔除掉
            entropy[j] = (None, 10000)

# 验证聚类中心查找结果
print('cluster_center:', cluster_center)
with open('../data/cluster_center.csv', 'wt') as wf:
    wf_csv = csv.writer(wf)
    headings = ['cluster_center', 'entropy']
    wf_csv.writerow(headings)
    for row in cluster_center:
        wf_csv.writerow(row)
