
--
-- Tablas generales (sin relaciones)
--

CREATE TABLE public.clientes (
	clienteid integer            	PRIMARY KEY		NOT NULL,
	tarjeta character varying(50) 					NOT NULL,
	saldo real 										NOT NULL,    
	email character varying(50),
	nombre character varying(50) 					NOT NULL,
	password character varying(50) 					NOT NULL
);

ALTER TABLE public.clientes OWNER TO alumnodb;

--

CREATE TABLE public.actores (
    actorid integer					PRIMARY KEY		NOT NULL,
    actor character varying(128) 					NOT NULL
);

ALTER TABLE public.actores OWNER TO alumnodb;

--

CREATE TABLE public.directores (
    directorid integer 				PRIMARY KEY		NOT NULL,
    director character varying(128) 				NOT NULL
);

ALTER TABLE public.directores OWNER TO alumnodb;

--

CREATE TABLE public.paises (
    paisid SERIAL					PRIMARY KEY		NOT NULL,
    pais character varying(32) 					    NOT NULL
);

ALTER TABLE public.paises OWNER TO alumnodb;

--

CREATE TABLE public.generos (
    generoid SERIAL 				PRIMARY KEY		NOT NULL,
    genero character varying(32) 					NOT NULL
);

ALTER TABLE public.generos OWNER TO alumnodb;

--

CREATE TABLE public.lenguas (
    lenguaid SERIAL 				PRIMARY KEY		NOT NULL,
    lengua character varying(32) 					NOT NULL
);

ALTER TABLE public.lenguas OWNER TO alumnodb;

--

CREATE TABLE public.peliculas (
    peliculaid integer 				PRIMARY KEY		NOT NULL,
    titulo character varying(255) 					NOT NULL,
    estreno text									NOT NULL
);

ALTER TABLE public.peliculas OWNER TO alumnodb;

--

CREATE TABLE public.pedidos (
    pedidoid integer 				PRIMARY KEY		NOT NULL,
    fecha date 										NOT NULL,
    clienteid integer				REFERENCES clientes(clienteid),
    precioneto numeric,
    impuestos numeric,
    preciototal numeric,
    estado character varying(10)
);

ALTER TABLE public.pedidos OWNER TO alumnodb;

--

CREATE TABLE public.productos (
    productoid integer 				PRIMARY KEY 	NOT NULL,
    peliculaid integer 				REFERENCES peliculas(peliculaid),
    precio numeric 							NOT NULL,
    descripcion character varying(30) 				NOT NULL,
    stock integer									NOT NULL,
    ventas integer 									NOT NULL
);

ALTER TABLE public.productos OWNER TO alumnodb;

--
-- Tablas para relaciones
--

CREATE TABLE public.detallespedidos (
    pedidoid integer 				REFERENCES pedidos(pedidoid),
    productoid integer 				REFERENCES productos(productoid),
    preciototal numeric,
    cantidad integer 								NOT NULL
);

ALTER TABLE public.detallespedidos OWNER TO alumnodb;

CREATE TABLE public.actorpeliculas (
    actorid integer 				REFERENCES actores(actorid),
    peliculaid integer 				REFERENCES peliculas(peliculaid),
    personaje text 									NOT NULL,
    esvoz smallint 			DEFAULT (0)::smallint 	NOT NULL
);

ALTER TABLE public.actorpeliculas OWNER TO alumnodb;

CREATE TABLE public.directorpeliculas (
    directorid integer 				REFERENCES directores(directorid),
    peliculaid integer 				REFERENCES peliculas(peliculaid)
);

ALTER TABLE public.directorpeliculas OWNER TO alumnodb;

CREATE TABLE public.lenguapeliculas (
    lenguaid integer 				REFERENCES lenguas(lenguaid),
    peliculaid integer 				REFERENCES peliculas(peliculaid)
);

ALTER TABLE public.lenguapeliculas OWNER TO alumnodb;

CREATE TABLE public.paispeliculas (
    paisid integer 					REFERENCES paises(paisid),
    peliculaid integer 				REFERENCES peliculas(peliculaid)
);

ALTER TABLE public.paispeliculas OWNER TO alumnodb;

CREATE TABLE public.generopeliculas (
    generoid integer 				REFERENCES generos(generoid),
    peliculaid integer 				REFERENCES peliculas(peliculaid)
);

ALTER TABLE public.generopeliculas OWNER TO alumnodb;

--
-- Copiar datos (hay que hacer 15)
--

INSERT INTO public.clientes (clienteid, tarjeta, saldo, email, nombre, password)
SELECT customerid, creditcard, 80, email, CONCAT(firstname, ' ', lastname) as fullname, password
FROM public.customers;

INSERT INTO public.actores (actorid, actor)
SELECT actorid, actorname 
FROM imdb_actors;

INSERT INTO public.directores (directorid, director)
SELECT directorid, directorname 
FROM imdb_directors;

INSERT INTO public.peliculas (peliculaid, titulo, estreno)
SELECT movieid, movietitle, year 
FROM imdb_movies;

INSERT INTO public.pedidos (pedidoid, fecha, clienteid, precioneto, impuestos, preciototal, estado)
SELECT orderid, orderdate, customerid, netamount, tax, totalamount, status 
FROM orders;

INSERT INTO public.paises (pais)
SELECT DISTINCT country 
FROM imdb_moviecountries;

INSERT INTO public.generos (genero)
SELECT DISTINCT genre 
FROM imdb_moviegenres;

INSERT INTO public.lenguas (lengua)
SELECT DISTINCT language 
FROM imdb_movielanguages;

INSERT INTO public.productos (productoid, peliculaid, precio, descripcion, stock, ventas)
SELECT products.prod_id, movieid, price, description,
    CASE WHEN inventory.stock is NULL THEN 0 ELSE inventory.stock END,
    CASE WHEN inventory.sales is NULL THEN 0 ELSE inventory.sales END
FROM products LEFT OUTER JOIN  inventory ON products.prod_id = inventory.prod_id;

INSERT INTO public.detallespedidos (pedidoid, productoid, preciototal, cantidad)
SELECT orderid, prod_id, price, quantity 
FROM orderdetail;

INSERT INTO public.actorpeliculas (actorid, peliculaid, personaje, esvoz)
SELECT actorid, movieid, "character", isvoice
FROM imdb_actormovies;

INSERT INTO public.directorpeliculas (directorid, peliculaid)
SELECT directorid, movieid
FROM imdb_directormovies;

INSERT INTO public.lenguapeliculas (lenguaid, peliculaid)
SELECT lenguaid, movieid
FROM lenguas INNER JOIN imdb_movielanguages ON lenguas.lengua = imdb_movielanguages.language;

INSERT INTO public.generopeliculas (generoid, peliculaid)
SELECT generoid, movieid
FROM generos INNER JOIN imdb_moviegenres ON generos.genero = imdb_moviegenres.genre;

INSERT INTO public.paispeliculas (paisid, peliculaid)
SELECT paisid, movieid
FROM paises INNER JOIN imdb_moviecountries ON paises.pais = imdb_moviecountries.country;

DROP TABLE customers, imdb_actormovies, imdb_actors, imdb_directormovies, imdb_directors,
imdb_moviecountries, imdb_moviegenres, imdb_movielanguages, imdb_movies, inventory, orderdetail, 
orders, products;