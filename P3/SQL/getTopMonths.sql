DROP FUNCTION IF EXISTS getTopMonths(integer, integer);

CREATE OR REPLACE FUNCTION getTopMonths(p integer, i integer) RETURNS TABLE(ano double precision, mes double precision, preciototal integer, cantidad integer) AS $$
BEGIN
	RETURN QUERY (SELECT * FROM (SELECT extract(year from fecha) as ano, extract(month from fecha) as mes, 
										cast(SUM(T2.preciototal) AS integer) AS preciototal, cast(SUM(T2.cantidad) AS integer) AS cantidad
								FROM pedidos AS T1, detallespedidos AS T2
								WHERE T1.pedidoid = T2.pedidoid
								GROUP BY ano, mes) AS T
								WHERE T.preciototal >= i OR T.cantidad >= p);
END;
$$ language plpgsql;
