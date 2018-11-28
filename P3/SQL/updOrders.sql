DROP 
  TRIGGER if exists updOrders on detallespedidos;
DROP 
  FUNCTION if exists updorders_function();
create 
or replace FUNCTION updOrders_function() RETURNS trigger AS $$ DECLARE result integer;
BEGIN IF (TG_OP = 'DELETE') THEN result := - OLD.preciototal;
UPDATE 
  pedidos 
SET 
  precioneto = precioneto + result, 
  preciototal = precioneto + result + impuestos 
WHERE 
  OLD.pedidoid = pedidoid;
RETURN OLD;
ELSIF (TG_OP = 'INSERT') THEN result := NEW.preciototal;
UPDATE 
  pedidos 
SET 
  precioneto = precioneto + result, 
  preciototal = precioneto + result + impuestos 
WHERE 
  NEW.pedidoid = pedidoid;
RETURN NEW;
ELSE result := NEW.preciototal - OLD.preciototal;
UPDATE 
  pedidos 
SET 
  precioneto = precioneto + result, 
  preciototal = precioneto + result + impuestos 
WHERE 
  NEW.pedidoid = pedidoid;
RETURN NEW;
END IF;
END;
$$ language plpgsql;
CREATE TRIGGER updOrders BEFORE INSERT 
OR 
UPDATE 
  OR DELETE ON detallespedidos FOR EACH ROW EXECUTE PROCEDURE updOrders_function();
