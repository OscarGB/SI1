-- EJD1
explain analyze select count(*) 
from orders 
where status is null;

-- EJD2
explain analyze select count(*) 
from orders 
where status ='Shipped';

CREATE INDEX bla on orders (status);

-- EJD3
explain analyze select count(*) 
from orders 
where status is null;

-- EJD4
explain analyze select count(*) 
from orders 
where status ='Shipped';

ANALYZE orders;

-- EJD5
explain analyze select count(*) 
from orders 
where status is null;

-- EJD6
explain analyze select count(*) 
from orders 
where status ='Shipped';

-- EJD7
explain analyze select count(*) 
from orders 
where status ='Paid';

-- EJD8
explain analyze select count(*) 
from orders 
where status ='Processed';