############### RMF值计算 #################

# R值计算
select
customerId,
datediff('2011-01-30',  MAX(invoiceDate)) as last_buy_date
from cleaned
GROUP by customerId;

# F值计算
select
customerId,
COUNT(DISTINCT(DATE(invoiceDate))) as total_buy_times
from cleaned
GROUP BY customerId;

# M值计算
select
customerId,
SUM(quantity * unitPrice)  / COUNT(DISTINCT(DATE(invoiceDate)))  as avg_money
from cleaned
GROUP BY customerId;

############ RMF值标准化 ###############

# 首先计算三者的极值
