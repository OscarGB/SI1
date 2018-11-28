DROP 
  TRIGGER if exists updInventory on pedidos;
DROP 
  FUNCTION if exists updInventory_function();
create 
or replace FUNCTION updInventory_function() RETURNS trigger AS $$ BEGIN IF (
  OLD.estado is null 
  and NEW.estado is not null
) THEN 
UPDATE 
  productos 
SET 
  stock = stock - cantidad, 
  ventas = ventas + cantidad 
FROM 
  detallespedidos 
WHERE 
  OLD.pedidoid = detallespedidos.pedidoid 
  and detallespedidos.productoid = productos.productoid;
DELETE FROM 
  alertas 
WHERE 
  productoid in (
    SELECT 
      productoid 
    FROM 
      detallespedidos 
    where 
      OLD.pedidoid = detallespedidos.pedidoid
  );
INSERT INTO alertas 
SELECT 
  productoid, 
  stock 
FROM 
  (
    SELECT 
      * 
    FROM 
      pedidos 
    where 
      pedidos.pedidoid = OLD.pedidoid
  ) AS T 
  inner join detallespedidos on detallespedidos.pedidoid = T.pedidoid natural 
  join productos 
WHERE 
  stock < 1;
END IF;
RETURN NEW;
END;
$$ language plpgsql;
CREATE TRIGGER updInventory 
AFTER 
UPDATE 
  ON pedidos FOR EACH ROW EXECUTE PROCEDURE updInventory_function();
