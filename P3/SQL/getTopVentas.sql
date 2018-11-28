CREATE 
OR REPLACE FUNCTION getTopVentas(year integer) RETURNS TABLE(
  ano integer, 
  cantidadtotal integer, 
  titulo character varying(255)
) AS $$ BEGIN RETURN QUERY(
  SELECT 
    T2.ano :: int, 
    T2.cantidadtotal :: int, 
    peliculas.titulo 
  FROM 
    (
      SELECT 
        T1.ano, 
        (
          array_agg(
            T1.peliculaid 
            ORDER BY 
              T1.cantidadtotal DESC
          )
        ) [1] as peliculaid, 
        MAX(T1.cantidadtotal) as cantidadtotal 
      FROM 
        (
          SELECT 
            extract(
              year 
              from 
                fecha
            ) as ano, 
            peliculaid, 
            SUM(cantidad) as cantidadtotal 
          FROM 
            (
              pedidos 
              INNER JOIN detallespedidos on pedidos.pedidoid = detallespedidos.pedidoid
            ) as T 
            INNER JOIN productos on T.productoid = productos.productoid 
          GROUP BY 
            ano, 
            peliculaid
        ) as T1 
      GROUP BY 
        T1.ano
    ) as T2 
    INNER JOIN peliculas on T2.peliculaid = peliculas.peliculaid 
  WHERE 
    T2.ano >= $1
);
END;
$$ language plpgsql;
