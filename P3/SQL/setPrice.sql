UPDATE public.detallespedidos
SET preciototal = detallespedidos.cantidad * productos.precio
FROM productos
WHERE productos.productoid = detallespedidos.productoid;