CREATE INDEX clientesDistintos ON orders (orderdate);

EXPLAIN 
ANALYZE
SELECT COUNT(DISTINCT customerid) as cc
FROM 
  orders 
WHERE
  orderdate >= to_date('201504', 'YYYYMM') 
  and orderdate < to_date('201504', 'YYYYMM') + interval '1 month'
  and totalamount > 100;
