CREATE 
OR REPLACE FUNCTION setOrderAmount() RETURNS void AS $$ BEGIN 
UPDATE 
  pedidos 
SET 
  precioneto = suma, 
  preciototal = suma + impuestos 
FROM 
  (
    SELECT 
      SUM(preciototal) as suma, 
      pedidoid 
    FROM 
      detallespedidos 
    GROUP BY 
      pedidoid
  ) AS T 
WHERE 
  T.pedidoid = pedidos.pedidoid 
  and (
    precioneto IS NULL 
    or preciototal IS NULL
  );
END;
$$ language plpgsql;
SELECT 
  * 
FROM 
  setOrderAmount();
