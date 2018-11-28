UPDATE 
  public.detallespedidos 
SET 
  preciototal = detallespedidos.cantidad * T.precio / POW(
    1.02, 
    extract(
      year 
      from 
        NOW()
    ) - extract(
      year 
      from 
        pedidos.fecha
    )
  ) 
FROM 
  (
    productos NATURAL 
    JOIN peliculas
  ) AS T, 
  pedidos 
WHERE 
  T.productoid = detallespedidos.productoid 
  and pedidos.pedidoid = detallespedidos.pedidoid;
