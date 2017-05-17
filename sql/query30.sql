############### RMF值计算 #################

# R值计算
select
customerId,
datediff('2011-12-09',  MAX(invoiceDate)) as last_buy_date_diff
from cleaned30
GROUP by customerId;

# F值计算
select
customerId,
COUNT(DISTINCT(DATE(invoiceDate))) as total_buy_times
from cleaned30
GROUP BY customerId;

# M值计算
select
customerId,
SUM(quantity * unitPrice)  / COUNT(DISTINCT(DATE(invoiceDate)))  as avg_money
from cleaned30
GROUP BY customerId;

############ RMF极值计算 ###############

# R的极值(Rmax, Rmin)计算 (315, 4)
SELECT
MAX(r.last_buy_date) as r_max, MIN(r.last_buy_date) as r_min
FROM (
select
customerId,
datediff('2011-12-09',  MAX(invoiceDate)) as last_buy_date
from cleaned30
GROUP by customerId
) as r;

# F的极值(Fmax)计算 13
SELECT
MAX(f.total_buy_times) as f_max
FROM (
select
customerId,
COUNT(DISTINCT(DATE(invoiceDate))) as total_buy_times
from cleaned30
GROUP BY customerId
) as f;

# M的极值(Mmax, Mmin)计算 (6207.67, 89)
SELECT
MAX(m.avg_money) as m_max, MIN(m.avg_money) as  m_min
FROM (
select
customerId,
SUM(quantity * unitPrice)  / COUNT(DISTINCT(DATE(invoiceDate)))  as avg_money
from cleaned30
GROUP BY customerId
) as m;

########### RMF标准化 ##############################

# 创建用于RFM原始值记录的表
CREATE TABLE rfm30(
`customer_id` VARCHAR(255) not null comment '顾客id',
`r` VARCHAR(255) not NULL comment 'R值',
`f` VARCHAR(255) not null comment 'F值',
`m` VARCHAR(255) not null COMMENT 'M值'
) Engine = InnoDB, Charset = utf8;

# 计算RFM原始值
INSERT INTO rfm30
SELECT
  r.customerId,
  r.last_buy_date_diff as R,
  f.total_buy_times as F,
  m.avg_money as M
FROM
  (select
  customerId,
  datediff('2011-12-09',  MAX(invoiceDate)) as last_buy_date_diff
  from cleaned30
  GROUP by customerId) as r,
  (select
  customerId,
  COUNT(DISTINCT(DATE(invoiceDate))) as total_buy_times
  from cleaned30
  GROUP BY customerId) as f,
  (select
  customerId,
  SUM(quantity * unitPrice)  / COUNT(DISTINCT(DATE(invoiceDate)))  as avg_money
  from cleaned30
  GROUP BY customerId) as m
WHERE r.customerId = f.customerId
AND  r.customerId = m.customerId;

# 创建RFM正规化值的表
CREATE TABLE rfm_regular30(
`customer_id` VARCHAR(255) not null comment '顾客id',
`r_regular` VARCHAR(255) not NULL comment 'R值',
`f_regular` VARCHAR(255) not null comment 'F值',
`m_regular` VARCHAR(255) not null COMMENT 'M值'
) Engine = InnoDB, Charset = utf8;

# 计算RFM正规化值
INSERT INTO
  rfm_regular30
SELECT
  customer_id,
  (315 - r) / (315 - 4) as r_regular,
  (f / 13) as f_regular,
  (m - (89)) / (6207.67 - (89)) as m_reguar
FROM rfm30;

# 创建RFM归一化的表
drop table rfm_normalize30;
CREATE TABLE rfm_normalize30(
`customer_id` VARCHAR(255) not null comment '顾客id',
`r_normalize` VARCHAR(255) not NULL comment 'R值归一化',
`f_normalize` VARCHAR(255) not null comment 'F值归一化',
`m_normalize` VARCHAR(255) not null COMMENT 'M值归一化'
) Engine = InnoDB, Charset = utf8;

# 计算RFM归一化的值
INSERT INTO
  rfm_normalize30
SELECT
  customer_id,
  r_regular / (r_regular + f_regular + m_regular),
  f_regular / (r_regular + f_regular + m_regular),
  m_regular / (r_regular + f_regular + m_regular)
FROM rfm_regular30
order by customer_id;

# rfm_normalize表, 异常数据清除
DELETE  from chen20170509.rfm_normalize30
WHERE
r_normalize <= 0 OR f_normalize <= 0 OR m_normalize <= 0

