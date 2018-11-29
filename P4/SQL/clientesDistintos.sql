CREATE INDEX clientesDistintos ON orders (orderdate);

EXPLAIN 
ANALYZE
SELECT 
  customers.* 
FROM 
  customers 
  inner join (
    SELECT 
      DISTINCT customerid 
    FROM 
      orders 
    where 
      orderdate >= to_date('201504', 'YYYYMM') 
      and orderdate < to_date('201504', 'YYYYMM') + interval '1 month'
      and totalamount > 100
  ) as T USING (customerid);
