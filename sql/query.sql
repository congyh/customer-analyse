############### RMF原始值计算 #################

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

############ RMF极值计算 ###############

# R的极值(Rmax, Rmin)计算
SELECT
MAX(r.last_buy_date) as r_max, MIN(r.last_buy_date) as r_min
FROM (
select
customerId,
datediff('2011-01-30',  MAX(invoiceDate)) as last_buy_date
from cleaned
GROUP by customerId
) as r;

# F的极值(Fmax)计算
SELECT
MAX(f.total_buy_times) as f_max
FROM (
select
customerId,
COUNT(DISTINCT(DATE(invoiceDate))) as total_buy_times
from cleaned
GROUP BY customerId
) as f;

# M的极值(Mmax, Mmin)计算
SELECT
MAX(m.avg_money) as m_max, MIN(m.avg_money) as  m_min
FROM (
select
customerId,
SUM(quantity * unitPrice)  / COUNT(DISTINCT(DATE(invoiceDate)))  as avg_money
from cleaned
GROUP BY customerId
) as m;

########### RMF标准化 ##############################

# TODO 标准化需要完成的任务是, 用每个顾客的RMF原始值, 用RMF极值进行一定的处理
# TODO 考虑建立视图, 或者临时表, 用子查询的话太罗嗦了.


